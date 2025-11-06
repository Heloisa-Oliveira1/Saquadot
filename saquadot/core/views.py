from django.shortcuts import render, get_object_or_404, redirect
from .models import Animal, Adocao, Campanha, Notificacao
from django.contrib.auth.decorators import login_required
from .forms import AdocaoForm, AnimalForm
from django.contrib import messages
from django.http import JsonResponse

def index(request):
    # Query base
    animais = Animal.objects.all()

    # Recebe filtros da querystring
    especie = request.GET.get('especie', '').strip()
    idade = request.GET.get('idade', '').strip()

    # Filtra por espécie (se informado)
    if especie:
        # usa __iexact para ignorar caixa; ajusta valores "Cachorro"/"cachorro"
        animais = animais.filter(especie__iexact=especie)

    # Filtra por idade (se informado e válido)
    if idade:
        try:
            idade_int = int(idade)
            animais = animais.filter(idade=idade_int)
        except (ValueError, TypeError):
            # se não for inteiro, devolve queryset vazio para não lançar erro
            animais = animais.none()

    # Opcional: ordenar (ex.: mais recentes primeiro)
    animais = animais.order_by('-id')

    # Renderiza (use 'core/index.html' se seu template estiver nessa pasta)
    return render(request, 'core/index.html', {'animais': animais})


def animal_detail(request, id):
    animal = get_object_or_404(Animal, id=id)
    return render(request, 'core/animal_detail.html', {'animal': animal})

def campanhas(request):
    campanhas = Campanha.objects.all()
    return render(request, 'core/campanhas.html', {'campanhas': campanhas})

def solicitar_adocao(request, id):
    # 1️⃣ Se o usuário não estiver logado, mostra o aviso de login
    if not request.user.is_authenticated:
        return render(request, 'core/adocao_login_necessario.html')

    # 2️⃣ Busca o animal no banco (ou erro 404 se não existir)
    animal = get_object_or_404(Animal, id=id)

    # 3️⃣ Impede o mesmo usuário de solicitar adoção duas vezes
    if Adocao.objects.filter(animal=animal, adotante=request.user).exists():
        return render(request, 'core/adocao_existente.html', {'animal': animal})

    # 4️⃣ Se o formulário for enviado (POST), salva o pedido
    if request.method == 'POST':
        form = AdocaoForm(request.POST)
        if form.is_valid():
            adocao = form.save(commit=False)
            adocao.adotante = request.user
            adocao.animal = animal
            adocao.save()
            return render(request, 'core/adocao_sucesso.html', {'animal': animal})
    else:
        form = AdocaoForm()

    # 5️⃣ Renderiza o formulário de confirmação
    return render(request, 'core/adocao_form.html', {'form': form, 'animal': animal})

@login_required
def cadastrar_animal(request):
    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES)
        if form.is_valid():
            animal = form.save(commit=False)
            animal.cuidador = request.user  # quem cadastrou
            animal.save()
            return redirect('home')
    else:
        form = AnimalForm()

    return render(request, 'core/animal_form.html', {'form': form})

# READ - Listar animais do cuidador
@login_required
def meus_animais(request):
    animais = Animal.objects.filter(cuidador=request.user)
    return render(request, 'core/meus_animais.html', {'animais': animais})


# ✏️ UPDATE - Editar animal
@login_required
def editar_animal(request, id):
    animal = get_object_or_404(Animal, id=id, cuidador=request.user)
    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES, instance=animal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Animal atualizado com sucesso! 🐾')
            return redirect('meus_animais')
    else:
        form = AnimalForm(instance=animal)
    return render(request, 'core/animal_form.html', {'form': form, 'editar': True})


# 🗑️ DELETE - Excluir animal
@login_required
def excluir_animal(request, id):
    animal = get_object_or_404(Animal, id=id, cuidador=request.user)
    if request.method == 'POST':
        animal.delete()
        messages.success(request, 'Animal excluído com sucesso! 🗑️')
        return redirect('meus_animais')
    return render(request, 'core/confirmar_exclusao.html', {'animal': animal})

# 👀 Listar pedidos de adoção pendentes
@login_required
def adocoes_pendentes(request):
    # Filtra apenas os pedidos de animais cadastrados pelo cuidador logado
    adocoes = Adocao.objects.filter(animal__cuidador=request.user)
    return render(request, 'core/adocoes_pendentes.html', {'adocoes': adocoes})

# ✅ Aprovar adoção
@login_required
def aprovar_adocao(request, id):
    adocao = get_object_or_404(Adocao, id=id, animal__cuidador=request.user)
    adocao.aprovado = True
    adocao.animal.adotado = True
    adocao.animal.save()
    adocao.save()

    # 📨 Cria a notificação para o adotante
    from .models import Notificacao
    mensagem = f"🎉 Sua adoção do animal {adocao.animal.nome} foi aprovada! Entre em contato com o cuidador para combinar a retirada."
    Notificacao.objects.create(usuario=adocao.adotante, mensagem=mensagem)

    messages.success(request, f"Adoção de {adocao.animal.nome} aprovada!")
    return redirect('adocoes_pendentes')

# ❌ Recusar adoção
@login_required
def recusar_adocao(request, id):
    adocao = get_object_or_404(Adocao, id=id, animal__cuidador=request.user)

    from .models import Notificacao
    mensagem = f"😿 Seu pedido de adoção do animal {adocao.animal.nome} foi recusado pelo cuidador."
    Notificacao.objects.create(usuario=adocao.adotante, mensagem=mensagem)

    adocao.delete()
    messages.warning(request, f"Pedido de adoção de {adocao.animal.nome} recusado.")
    return redirect('adocoes_pendentes')

# Listar as notificações
@login_required
def notificacoes(request):
    notificacoes = request.user.notificacoes.all().order_by('-data')
    return render(request, 'core/notificacoes.html', {'notificacoes': notificacoes})

from django.contrib.auth.decorators import login_required
from .models import Adocao

# 👤 Adotante: listar as próprias solicitações
@login_required
def minhas_solicitacoes(request):
    adocoes = Adocao.objects.filter(adotante=request.user).select_related('animal', 'animal__cuidador')
    
    # Esconde o contato se a adoção ainda não foi aprovada
    for adocao in adocoes:
        if not adocao.aprovado:
            adocao.animal.contato = None

    return render(request, 'core/minhas_solicitacoes.html', {'adocoes': adocoes})


# ❌ Retirar (cancelar) pedido de adoção
@login_required
def retirar_pedido(request, id):
    adocao = get_object_or_404(Adocao, id=id, adotante=request.user)
    animal_nome = adocao.animal.nome
    adocao.delete()

    from django.contrib import messages
    messages.warning(request, f"Sua solicitação de adoção de {animal_nome} foi retirada.")
    return redirect('minhas_solicitacoes')

# 📨 Página de notificações do usuário
@login_required
def notificacoes(request):
    notificacoes_nao_lidas = Notificacao.objects.filter(usuario=request.user, lida=False).order_by('-data')
    notificacoes_lidas = Notificacao.objects.filter(usuario=request.user, lida=True).order_by('-data')

    return render(request, 'core/notificacoes.html', {
        'notificacoes_nao_lidas': notificacoes_nao_lidas,
        'notificacoes_lidas': notificacoes_lidas,
    })

# ✅ Marcar uma notificação como lida
@login_required
def marcar_lida(request, id):
    notificacao = get_object_or_404(Notificacao, id=id, usuario=request.user)
    notificacao.lida = True
    notificacao.save()

    # Retorna JSON se for uma requisição AJAX (fetch)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        nao_lidas = Notificacao.objects.filter(usuario=request.user, lida=False).count()
        return JsonResponse({'success': True, 'notificacoes_nao_lidas': nao_lidas})

    messages.success(request, "Notificação marcada como lida.")
    return redirect('notificacoes')


# 🧹 Marcar todas como lidas
@login_required
def marcar_todas_lidas(request):
    Notificacao.objects.filter(usuario=request.user, lida=False).update(lida=True)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'notificacoes_nao_lidas': 0})

    messages.success(request, "Todas as notificações foram marcadas como lidas.")
    return redirect('notificacoes')

@login_required
def apagar_historico(request):
    # Apaga apenas notificações que já foram lidas
    Notificacao.objects.filter(usuario=request.user, lida=True).delete()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True})

    messages.success(request, "Histórico de notificações apagado com sucesso.")
    return redirect('notificacoes')
