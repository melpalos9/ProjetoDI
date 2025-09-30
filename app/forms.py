from django import forms
from .models import Diario

class DiarioForm(forms.ModelForm):
    class Meta:
        model = Diario
        fields = ["titulo", "conteudo"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control", "placeholder": "Título"}),
            "conteudo": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Escreva aqui..."}),
        }
