from django.db import models

# Modèle utilisateur existant
class Utilisateur(models.Model):
    nom = models.CharField(max_length=50)
    mot_de_passe = models.CharField(max_length=50)

    def __str__(self):
        return self.nom

# Modèle Game
class Game(models.Model):
    GENRES = [
        ('RPG', 'RPG'),
        ('FPS', 'FPS'),
        ('Aventure', 'Aventure'),
        ('Stratégie', 'Stratégie'),
        ('Autre', 'Autre'),
    ]

    AMBIANCES = [
        ('Cyberpunk', 'Cyberpunk'),
        ('Fantasy', 'Fantasy'),
        ('Post-apocalyptique', 'Post-apocalyptique'),
        ('Historique', 'Historique'),
        ('Autre', 'Autre'),
    ]

    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE,related_name="auth_games")
    genre = models.CharField(max_length=50, choices=GENRES)
    ambiance = models.CharField(max_length=50, choices=AMBIANCES)
    mots_cles = models.CharField(max_length=200)
    references = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.genre} - {self.ambiance} ({self.user.nom})"