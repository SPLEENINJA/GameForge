from django import forms
import json

GENRES = [
    ('RPG', 'RPG'),
    ('FPS', 'FPS'),
    ('Metroidvania', 'Metroidvania'),
    ('Visual Novel', 'Visual Novel'),
]

AMBIANCES = [
    ('Post-apo', 'Post-apo'),
    ('Guerre', 'Guerre'),
    ('Cyberpunk', 'Cyberpunk'),
    ('Dark fantasy', 'Dark fantasy'),
]

class GameInfoForm(forms.Form):
    genre = forms.ChoiceField(choices=GENRES, label="Genre du jeu")
    ambiance = forms.ChoiceField(choices=AMBIANCES, label="Ambiance visuelle et narrative")
    mots_cles = forms.CharField(
        label="Mots-clés thématiques",
        help_text="Séparez les mots-clés par des virgules.",
        widget=forms.TextInput(attrs={"placeholder": "boucle temporelle, vengeance, IA rebelle..."})
    )
    references = forms.CharField(
        required=False,
        label="Références culturelles (facultatif)",
        help_text="Séparez les références par des virgules.",
        widget=forms.TextInput(attrs={"placeholder": "Zelda, Hollow Knight, Disco Elysium..."})
    )

    def to_json(self):
        """Retourne un dictionnaire JSON nettoyé pour les modèles IA."""
        data = {
            "genre": self.cleaned_data["genre"],
            "ambiance": self.cleaned_data["ambiance"],
            "mots_cles": [kw.strip() for kw in self.cleaned_data["mots_cles"].split(",") if kw.strip()],
            "references": [ref.strip() for ref in self.cleaned_data.get("references", "").split(",") if ref.strip()],
        }
        return json.dumps(data, ensure_ascii=False, indent=2)
