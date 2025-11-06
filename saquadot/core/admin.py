from django.contrib import admin
from .models import Animal, Adocao, Campanha

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'especie', 'idade', 'adotado', 'cuidador')
    list_filter = ('especie', 'adotado')
    search_fields = ('nome', 'descricao')

@admin.register(Adocao)
class AdocaoAdmin(admin.ModelAdmin):
    list_display = ('animal', 'adotante', 'data_pedido', 'aprovado')
    list_filter = ('aprovado',)
    search_fields = ('animal__nome', 'adotante__username')

@admin.register(Campanha)
class CampanhaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_evento', 'local', 'tipo')
    list_filter = ('tipo',)
    search_fields = ('titulo', 'descricao')
