from django import forms
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Game

class CustomUserCreationForm(UserCreationForm):
    password1=forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete':'new-password'})
    )
    password2=forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'autocomplete':'new-password'}),
        strip=False,
    )
    
    class Meta(UserCreationForm.Meta):
        fields=UserCreationForm.Meta.fields +("password1","password2")


from django import forms
from .models import Game

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['genre', 'ambiance', 'mots_cles', 'references']
        widgets = {
            'mots_cles': forms.TextInput(attrs={'placeholder': 'Ex: exploration, magie, énigmes'}),
            'references': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ex: Zelda, Skyrim… (facultatif)'}),
        }