from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .form import CustomUserCreationForm,GameForm
from django.contrib.auth.decorators import login_required
from .form import GameForm

from .models import Utilisateur, Game

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .form import GameForm

def inscription(request):
    if request.user.is_authenticated:
        return redirect('accueil')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Inscription réussie !')
            return redirect('accueil')
    else:
        form = CustomUserCreationForm()
    return render(request, 'inscription.html', {'form': form})

def connexion(request):
    if request.user.is_authenticated:
        return redirect('accueil')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenue {username} !')
            return redirect('accueil')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    return render(request, 'connexion.html')
@login_required
def accueil(request):
    return render(request, 'accueil.html')

def deconnexion(request):
    logout(request)
    return redirect('connexion')


# ---------------- Création de jeu ----------------
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Utilisateur, Game
from .form import GameForm

def create_game(request):
    # Vérifier que l'utilisateur est connecté
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('connexion')

    user = Utilisateur.objects.get(id=user_id)

    # Formulaire POST
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.user = user
            game.save()
            messages.success(request, "Jeu enregistré !")
            return redirect('create_game')
        else:
            print(form.errors)
    else:
        form = GameForm()

    # Lister les jeux de l'utilisateur
    games = Game.objects.filter(user=user)

    return render(request, 'auth_app/game_page.html', {'form': form, 'games': games})