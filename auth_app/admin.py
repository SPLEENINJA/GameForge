from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Utilisateur, Game

# Enregistrement dans l'admin
admin.site.register(Utilisateur)
admin.site.register(Game)