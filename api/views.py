# GameForge/api/views.py
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Game, GameProject, Favorite, UserUsage, GameConcept
from .serializers import GameProjectSerializer, GameSerializer, FavoriteSerializer, GameConceptSerializer
from .tasks import generate_full_project_task  
from rest_framework import status, generics, permissions
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from .orchestrator import generate_game_concept
import random

class GameConceptListCreateView(generics.ListCreateAPIView):
    serializer_class = GameConceptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GameConcept.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        print("🟢 Incoming game data:", self.request.data)
        if not serializer.is_valid():
            print("❌ Serializer validation failed:", serializer.errors)
        serializer.save(user=self.request.user)

class GenerateGameView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("🟢 Incoming data:", request.data)
        title = request.data.get("title")
        genre = request.data.get("genre")
        theme = request.data.get("atmosphere")
        inspiration = request.data.get("visual_style")
        # main_story = request.data.get("main_story")

        generated = generate_game_concept(title, genre, theme, inspiration)
        # 👇 Your AI orchestrator placeholder
        generated_game = {
            "title": f"Generated Game Concept: {title}",
            "genre": genre,
            "atmosphere": theme or "",
            "visual_style": inspiration or "",
            "main_story": generated.get("main_story"), #"This is a placeholder story for your game.",  # correct field main_story,#
            "characters": generated.get("characters"),
            "image": generated.get("image"),  # ✅ add image
            "is_public": True,
    }
        print("🧩 Serializer - fields:", GameSerializer().get_fields().keys())
        serializer = GameSerializer(data=generated_game)
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# class GenerateGameView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         title = request.data.get("title")
#         genre = request.data.get("genre")
#         theme = request.data.get("theme")
#         inspiration = request.data.get("inspiration")

#         # 👇 Replace with your AI orchestrator call
#         generated_game = {
#             "title": f"Generated Game Concept: {title}",
#             "genre": genre,
#             "theme": theme,
#             "inspiration": inspiration,
#             "story": "This is a placeholder story for your game.",
#             "characters": [
#                 {"name": "Character 1", "role": "Hero"},
#                 {"name": "Character 2", "role": "Villain"},
#             ],
#             "image": "https://example.com/placeholder-image.jpg",
#         }

#         # Save to Game model automatically
#         serializer = GameSerializer(data=generated_game)
#         if serializer.is_valid():
#             serializer.save(creator=request.user)
#             return Response(serializer.data, status=200)
#         else:
#             return Response({"error": serializer.errors}, status=400)        
    
# class GenerateGameView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         title = request.data.get("title")
#         genre = request.data.get("genre")
#         theme = request.data.get("theme")
#         inspiration = request.data.get("inspiration")

#         if not title or not genre or not theme or not inspiration:
#             return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

#         # Call the AI logic to generate game concept
#         generated_game = generate_game_concept(title, genre, theme, inspiration)

#         return Response(generated_game, status=status.HTTP_200_OK)
    


# class GenerateGameView(APIView):
#     permission_classes = [IsAuthenticated] # [AllowAny]

#     def post(self, request):
#         data = request.data
#         title = data.get("title", "Untitled Game")
#         genre = data.get("genre", "Adventure")
#         theme = data.get("theme", "Fantasy")
#         inspiration = data.get("inspiration", "Epic quests")
#         print(title + ',' + theme)
#          # AI logic to generate game concept here
#         generated_game = generate_game_concept(title, genre, theme, inspiration)

#         return Response(generated_game, status=status.HTTP_200_OK)
    

        # STUB: generate fake game concept (replace with AI later)
        # story = f"{title} is a {genre} game with a {theme} theme inspired by {inspiration}."
        # characters = [
        #     {"name": "Aria", "role": "Hero"},
        #     {"name": "Drax", "role": "Villain"},
        # ]
        # image_url = "https://via.placeholder.com/300x200.png?text=Concept+Art"

        # response = {
        #     "title": title,
        #     "genre": genre,
        #     "theme": theme,
        #     "inspiration": inspiration,
        #     "story": story,
        #     "characters": characters,
        #     "image": image_url,
        # }

        # return Response(response)

class IsOwnerOrPublic(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.privacy == GameProject.PRIVACY_PUBLIC:
            return True
        return request.user and request.user.is_authenticated and obj.owner == request.user

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = GameProject.objects.all().order_by("-created_at")
    serializer_class = GameProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ("retrieve",):
            return [IsOwnerOrPublic()]
        return super().get_permissions()

    def perform_create(self, serializer):
        proj = serializer.save(owner=self.request.user, ai_generation_status="queued")
        # Basic quota check
        usage, _ = UserUsage.objects.get_or_create(user=self.request.user)
        estimated_cost = 10
        if usage.credits < estimated_cost:
            proj.ai_generation_status = "error"
            proj.ai_error = "Insufficient credits"
            proj.save()
            raise PermissionError("Insufficient credits")
        usage.credits -= estimated_cost
        usage.save()
        # enqueue a background generation task
        generate_full_project_task.delay(str(proj.id))

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk=None):
        project = get_object_or_404(GameProject, id=pk)
        favorite, created = Favorite.objects.get_or_create(user=request.user, project=project)
        return Response({"favorited": created})

    @action(detail=False, methods=["get"], permission_classes=[permissions.AllowAny])
    def public(self, request):
        qs = GameProject.objects.filter(privacy=GameProject.PRIVACY_PUBLIC).order_by("-created_at")
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all().order_by('-created_at')
    serializer_class = GameSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def create(self, request, *args, **kwargs):
        print("🟢 Incoming game data:", request.data)
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("❌ Validation errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(creator=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        user = self.request.user
        if self.request.user.is_authenticated:
            return Game.objects.filter(is_public=True) | Game.objects.filter(creator=user)
        return Game.objects.filter(is_public=True)

# class GameViewSet(viewsets.ModelViewSet):
#     queryset = Game.objects.all().order_by('-created_at')
#     serializer_class = GameSerializer

#     def perform_create(self, serializer):
#         serializer.save(creator=self.request.user)

#     def get_queryset(self):
#         user = self.request.user
#         if self.request.user.is_authenticated:
#             return Game.objects.filter(is_public=True) | Game.objects.filter(creator=user)
#         return Game.objects.filter(is_public=True)

#     @action(detail=True, methods=['post'])
#     def toggle_privacy(self, request, pk=None):
#         game = self.get_object()
#         if game.creator != request.user:
#             return Response({'error': 'Unauthorized'}, status=403)
#         game.is_public = not game.is_public
#         game.save()
#         return Response({'status': 'privacy toggled', 'is_public': game.is_public})


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



# REGISTER
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=201)
        else:
            print("❌ Serializer errors:", serializer.errors)  # 👈 ADD THIS LINE
            return Response(serializer.errors, status=400)
# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [permissions.AllowAny]

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class RegisterView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         email = request.data.get('email')

#         if not username or not password:
#             return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

#         if User.objects.filter(username=username).exists():
#             return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

#         user = User.objects.create_user(username=username, password=password, email=email)
#         user.save()

#         refresh = RefreshToken.for_user(user)
#         return Response({
#             'message': 'User registered successfully.',
#             'user': {
#                 'id': user.id,
#                 'username': user.username,
#                 'email': user.email,
#             },
#             'tokens': {
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             }
#         }, status=status.HTTP_201_CREATED)

# LOGIN
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Login successful.",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
        }, status=status.HTTP_200_OK)


# LOGOUT (token blacklist)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # requires SimpleJWT blacklist app if enabled
            return Response({"message": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"error": "Invalid token or logout failed."}, status=status.HTTP_400_BAD_REQUEST)


# CURRENT USER
class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }, status=status.HTTP_200_OK)
