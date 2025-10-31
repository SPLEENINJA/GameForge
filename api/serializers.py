# api/serializers.py
from rest_framework import serializers
from .models import GameProject, Character, Asset, Favorite
from .models import Game, Favorite, GameConcept
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
    creator = serializers.ReadOnlyField(source='creator.username')
    story = serializers.CharField(write_only=True, required=False, allow_blank=True)
    theme = serializers.CharField(source='atmosphere', required=False, allow_blank=True)
    inspiration = serializers.CharField(source='visual_style', required=False, allow_blank=True)
    image = serializers.CharField(required=False)
    class Meta:
        model = Game
        fields = [
            'id',
            'creator',
            'title',
            'genre',
            'theme',
            'atmosphere',
            'inspiration',
            'visual_style',
            'story',          # input only
            'main_story',     # stored in DB
            'characters',
            'concept_art_character',
            'concept_art_environment',
            'is_public',
            'created_at',
            'image',
        ]
        read_only_fields = ['creator', 'created_at']

    def validate(self, data):
        # If story is missing but main_story is not, raise validation error
        if not data.get('story') and not data.get('main_story'):
            raise serializers.ValidationError({
                "story": "Either 'story' or 'main_story' must be provided."
            })
        return data

    def create(self, validated_data):
        if 'story' in validated_data:
            validated_data['main_story'] = validated_data.pop('story')
        return super().create(validated_data)



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

class GameConceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameConcept
        fields = '__all__'
        read_only_fields = ('user', 'created_at')