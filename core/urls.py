from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('animal/<int:id>/', views.animal_detail, name='animal_detail'),
    path('campanhas/', views.campanhas, name='campanhas'),
    path('adotar/<int:id>/', views.solicitar_adocao, name='solicitar_adocao'),
    path('animal/cadastrar/', views.cadastrar_animal, name='cadastrar_animal'),
    
    # 🧩 CRUD
    path('meus-animais/', views.meus_animais, name='meus_animais'),
    path('animal/editar/<int:id>/', views.editar_animal, name='editar_animal'),
    path('animal/excluir/<int:id>/', views.excluir_animal, name='excluir_animal'),
    path('animal/foto/remover/<int:id>/', views.remover_foto_extra, name='remover_foto_extra'),

    # 🧾 Adoções
    path('adocoes/pendentes/', views.adocoes_pendentes, name='adocoes_pendentes'),
    path('adocao/aprovar/<int:id>/', views.aprovar_adocao, name='aprovar_adocao'),
    path('adocao/recusar/<int:id>/', views.recusar_adocao, name='recusar_adocao'),
    path('adocao/desfazer/<int:id>/', views.desfazer_adocao, name='desfazer_adocao'),

    # Adoções do adotante
    path('minhas-solicitacoes/', views.minhas_solicitacoes, name='minhas_solicitacoes'),
    path('retirar-pedido/<int:id>/', views.retirar_pedido, name='retirar_pedido'),

    # Notificações
    path('notificacoes/', views.notificacoes, name='notificacoes'),
    path('notificacoes/lida/<int:id>/', views.marcar_lida, name='marcar_lida'),
    path('notificacoes/todas-lidas/', views.marcar_todas_lidas, name='marcar_todas_lidas'),
    path('notificacoes/apagar-historico/', views.apagar_historico, name='apagar_historico'),
]
