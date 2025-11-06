from .models import Adocao, Notificacao

def contagem_pedidos(request):
    if request.user.is_authenticated:
        pendentes = Adocao.objects.filter(animal__cuidador=request.user, aprovado=False).count()
        return {'pedidos_pendentes': pendentes}
    return {}

def contagem_notificacoes(request):
    if request.user.is_authenticated:
        nao_lidas = Notificacao.objects.filter(usuario=request.user, lida=False).count()
        return {'notificacoes_nao_lidas': nao_lidas}
    return {}
