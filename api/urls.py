# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GenerateGameView
from .views import GameConceptListCreateView
from .views import (
    ProjectViewSet, GameViewSet, FavoriteViewSet,
    RegisterView, LoginView, LogoutView, UserView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'games', GameViewSet)
router.register(r'favorites', FavoriteViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', UserView.as_view(), name='user'),
    path("generate-game/", GenerateGameView.as_view(), name="generate-game"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('games/', GameConceptListCreateView.as_view(), name='game-list-create'),
]




# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import ProjectViewSet, GameViewSet, FavoriteViewSet

# router = DefaultRouter()
# router.register(r"projects", ProjectViewSet, basename="projects")
# router.register(r'games', GameViewSet)
# router.register(r'favorites', FavoriteViewSet)

# urlpatterns = router.urls
# urlpatterns = [
#     path('register/', RegisterView.as_view(), name='register'),
#     path('login/', LoginView.as_view(), name='login'),
#     path('logout/', LogoutView.as_view(), name='logout'),
#     path('user/', UserView.as_view(), name='user'),
# ]
# urlpatterns = [
#     path("", include(router.urls)),
# ]
