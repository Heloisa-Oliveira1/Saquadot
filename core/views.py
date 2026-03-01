from django.shortcuts import render, get_object_or_404, redirect
from .models import Animal, Adocao, Campanha, Notificacao, AnimalFoto
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import AdocaoForm, AnimalForm
from django.contrib import messages
from django.http import JsonResponse

def index(request):
    # Query base
    animais = Animal.objects.filter(adotado=False)

    # Recebe filtros da querystring
    especie = request.GET.get('especie', '').strip()
    idade = request.GET.get('idade', '').strip()
    porte = request.GET.get('porte', '').strip()
    sexo = request.GET.get('sexo', '').strip()

    # Filtra por espécie (se informado)
    if especie:
        # usa __iexact para ignorar caixa; ajusta valores "Cachorro"/"cachorro"
        animais = animais.filter(especie__iexact=especie)

    # Filtra por idade (se informado e válido)
    if idade:
        animais = animais.filter(idade=idade)

    # Filtra por porte (se informado)
    if porte:
        animais = animais.filter(porte__iexact=porte)

    # Filtra por sexo (se informado)
    if sexo:
        animais = animais.filter(sexo__iexact=sexo)

    # Opcional: ordenar (ex.: mais recentes primeiro)
    animais = animais.order_by('-id')

    # 📄 Paginação (6 animais por página)
    paginator = Paginator(animais, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Contexto extra para badges funcionarem na Home (se usuário logado)
    context = {
        'page_obj': page_obj,
        'idade_choices': Animal.IDADE_CHOICES,
        'porte_choices': Animal.PORTE_CHOICES,
        'sexo_choices': Animal.SEXO_CHOICES,
    }
    if request.user.is_authenticated:
        context['notificacoes_nao_lidas'] = Notificacao.objects.filter(usuario=request.user, lida=False).count()
        # Se o usuário for cuidador, contar pedidos pendentes (lógica simplificada)
        # Idealmente isso iria para um Context Processor
        context['pedidos_pendentes'] = Adocao.objects.filter(animal__cuidador=request.user, aprovado=False).count()
        # Lista de IDs dos animais que o usuário já solicitou adoção
        context['animais_solicitados'] = Adocao.objects.filter(adotante=request.user).values_list('animal_id', flat=True)
        # Lista de IDs dos animais que já foram APROVADOS para este usuário
        context['animais_aprovados'] = Adocao.objects.filter(adotante=request.user, aprovado=True).values_list('animal_id', flat=True)

    return render(request, 'core/index.html', context)


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

            # Salvar fotos extras
            for f in request.FILES.getlist('fotos_extras'):
                AnimalFoto.objects.create(animal=animal, imagem=f)

            return redirect('home')
    else:
        form = AnimalForm()

    return render(request, 'core/animal_form.html', {'form': form})

# READ - Listar animais do cuidador
@login_required
def meus_animais(request):
    status = request.GET.get('status')
    animais = Animal.objects.filter(cuidador=request.user)

    if status == 'adotados':
        animais = animais.filter(adotado=True)
    elif status == 'disponiveis':
        animais = animais.filter(adotado=False)

    return render(request, 'core/meus_animais.html', {'animais': animais, 'status': status})


# ✏️ UPDATE - Editar animal
@login_required
def editar_animal(request, id):
    animal = get_object_or_404(Animal, id=id, cuidador=request.user)
    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES, instance=animal)
        if form.is_valid():
            form.save()

            # Adicionar novas fotos extras (se houver)
            for f in request.FILES.getlist('fotos_extras'):
                AnimalFoto.objects.create(animal=animal, imagem=f)

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

# ↩️ Desfazer aprovação de adoção
@login_required
def desfazer_adocao(request, id):
    # Garante que o cuidador só possa desfazer adoções de seus próprios animais
    adocao = get_object_or_404(Adocao, id=id, animal__cuidador=request.user)

    # Reverte os status para pendente e não adotado
    adocao.aprovado = False
    adocao.animal.adotado = False
    adocao.animal.save()
    adocao.save()

    # 📨 Notifica o adotante sobre o cancelamento da aprovação
    mensagem = f"⚠️ A aprovação da adoção de {adocao.animal.nome} foi desfeita pelo cuidador. Por favor, aguarde novo contato."
    Notificacao.objects.create(usuario=adocao.adotante, mensagem=mensagem)

    messages.warning(request, f"A aprovação da adoção de {adocao.animal.nome} foi desfeita.")
    return redirect('adocoes_pendentes')

from django.contrib.auth.decorators import login_required
from .models import Adocao

# 👤 Adotante: listar as próprias solicitações
@login_required
def minhas_solicitacoes(request):
    adocoes = Adocao.objects.filter(adotante=request.user).select_related('animal', 'animal__cuidador')
    
    # Esconde o contato se a adoção ainda não foi aprovada
    for adocao in adocoes:
        if not adocao.aprovado:
            adocao.animal.whatsapp = None
            adocao.animal.email = None

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

# 🗑️ Remover foto extra específica
@login_required
def remover_foto_extra(request, id):
    foto = get_object_or_404(AnimalFoto, id=id)
    animal_id = foto.animal.id
    
    # Segurança: verifica se o animal pertence ao usuário logado
    if foto.animal.cuidador != request.user:
        messages.error(request, "Você não tem permissão para excluir esta foto.")
        return redirect('meus_animais')

    foto.delete()
    messages.success(request, "Foto removida com sucesso!")
    return redirect('editar_animal', id=animal_id)
