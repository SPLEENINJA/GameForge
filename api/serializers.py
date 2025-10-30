# api/serializers.py
from rest_framework import serializers
from .models import GameProject, Character, Asset, Favorite
from .models import Game, Favorite
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ["id", "file", "purpose", "generated_by", "created_at"]

class CharacterSerializer(serializers.ModelSerializer):
    art = AssetSerializer(read_only=True)
    class Meta:
        model = Character
        fields = ["id", "name", "role", "char_class", "background", "gameplay_style", "art"]

class GameProjectSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source="owner.username", read_only=True)
    characters = CharacterSerializer(many=True, read_only=True)
    assets = AssetSerializer(many=True, read_only=True)

    class Meta:
        model = GameProject
        fields = [
            "id", "owner_username", "title", "description", "genre", "visual_style", "keywords",
            "privacy", "created_at", "updated_at", "universe_text", "story_text", "pitch_deck",
            "ai_generation_status", "characters", "assets",
        ]
        read_only_fields = ["owner_username", "ai_generation_status", "characters", "assets"]

class GameSerializer(serializers.ModelSerializer):
    creator_username = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = Game
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"]
        )
        return user
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)