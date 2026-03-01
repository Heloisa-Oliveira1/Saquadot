from django import forms
from .models import Adocao, Animal

class AdocaoForm(forms.ModelForm):
    class Meta:
        model = Adocao
        fields = []

class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        
        fields = [
            'nome', 
            'especie', 
            'porte', 
            'sexo', 
            'idade', 
            'descricao', 
            'whatsapp',  
            'email',     
            'foto'
        ]
        
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
            'whatsapp': forms.TextInput(attrs={'placeholder': '(XX) XXXXX-XXXX'}),
            'email': forms.EmailInput(attrs={'placeholder': 'exemplo@email.com'}),
        }
