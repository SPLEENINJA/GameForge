# api/admin.py
from django.contrib import admin
from .models import GameProject, Character, Asset, Favorite, UserUsage

admin.site.register(GameProject)
admin.site.register(Character)
admin.site.register(Asset)
admin.site.register(Favorite)
admin.site.register(UserUsage)
