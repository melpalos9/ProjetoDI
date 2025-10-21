from django import forms
from .models import Diario, Feedback

class DiarioForm(forms.ModelForm):
    class Meta:
        model = Diario
        fields = ['titulo', 'conteudo']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título da entrada'}),
            'conteudo': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escreva seus pensamentos...', 'rows': 4}),
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['comentario', 'nota']
        widgets = {
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Deixe seu feedback...', 'rows': 4}),
            'nota': forms.Select(attrs={'class': 'form-control'}),
        }