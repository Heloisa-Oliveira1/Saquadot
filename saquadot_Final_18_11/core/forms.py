from django import forms
from .models import Adocao, Animal

class AdocaoForm(forms.ModelForm):
    class Meta:
        model = Adocao
        fields = []  # sem campos visíveis — apenas o botão “Confirmar adoção”

class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['nome', 'especie', 'idade', 'descricao', 'foto', 'contato']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }

