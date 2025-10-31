# api/models.py
import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

User = settings.AUTH_USER_MODEL

class Game(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games')
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    atmosphere = models.CharField(max_length=200, blank=True)
    visual_style = models.CharField(max_length=200, blank=True)
    main_story = models.TextField()
    characters = models.JSONField(default=list)  # [{"name": "...", "role": "..."}]
    concept_art_character = models.ImageField(upload_to='art/characters/', blank=True, null=True)
    concept_art_environment = models.ImageField(upload_to='art/environments/', blank=True, null=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='generated_art/', null=True, blank=True)

    def __str__(self):
        return self.title
    
class GameConcept(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="game_concepts")
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    theme = models.CharField(max_length=100)
    inspiration = models.TextField(blank=True)
    story = models.TextField()
    characters = models.JSONField(default=list)
    image = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.user.username}"
    
class GameProject(models.Model):
    PRIVACY_PUBLIC = "public"
    PRIVACY_PRIVATE = "private"
    PRIVACY_CHOICES = [(PRIVACY_PUBLIC, "Public"), (PRIVACY_PRIVATE, "Private")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    genre = models.CharField(max_length=100, blank=True)
    visual_style = models.CharField(max_length=200, blank=True)
    keywords = models.TextField(blank=True)
    privacy = models.CharField(max_length=20, choices=PRIVACY_CHOICES, default=PRIVACY_PUBLIC)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    universe_text = models.JSONField(null=True, blank=True)
    story_text = models.JSONField(null=True, blank=True)
    pitch_deck = models.JSONField(null=True, blank=True)
    ai_generation_status = models.CharField(max_length=50, default="pending")
    ai_error = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title or 'Untitled'} ({self.owner})"

class Character(models.Model):
    project = models.ForeignKey(GameProject, on_delete=models.CASCADE, related_name="characters")
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120, blank=True)
    char_class = models.CharField(max_length=80, blank=True)
    background = models.TextField(blank=True)
    gameplay_style = models.TextField(blank=True)
    art = models.ForeignKey('Asset', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')

class Asset(models.Model):
    project = models.ForeignKey(GameProject, on_delete=models.CASCADE, related_name="assets")
    file = models.ImageField(upload_to="game_assets/%Y/%m/%d/")
    purpose = models.CharField(max_length=50, help_text="character_art, environment, thumbnail")
    generated_by = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'game')


class UserUsage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="usage")
    credits = models.IntegerField(default=100)
    last_reset = models.DateTimeField(default=timezone.now)
