from django.db import models
from django.contrib.auth.models import User

class Animal(models.Model):
    nome = models.CharField(max_length=100)
    especie = models.CharField(max_length=50, choices=[('Cachorro', 'Cachorro'), ('Gato', 'Gato')])
    idade = models.IntegerField()
    descricao = models.TextField()
    foto = models.ImageField(upload_to='animais/')
    adotado = models.BooleanField(default=False)
    cuidador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='animais')

    # Campo de contato
    contato = models.CharField(
    max_length=100,
    blank=True,
    null=True,
    help_text="Telefone ou WhatsApp para contato"
)
    def __str__(self):
        return self.nome

class Adocao(models.Model):
    adotante = models.ForeignKey(User, on_delete=models.CASCADE)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    data_pedido = models.DateTimeField(auto_now_add=True)
    aprovado = models.BooleanField(default=False)

    def __str__(self):
        return f"Adoção de {self.animal.nome} por {self.adotante.username}"

class Campanha(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    data_evento = models.DateField()
    local = models.CharField(max_length=200)
    tipo = models.CharField(max_length=50, choices=[('Vacinação', 'Vacinação'), ('Adoção', 'Adoção')])

    def __str__(self):
        return self.titulo

class Notificacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificacoes')
    mensagem = models.CharField(max_length=255)
    data = models.DateTimeField(auto_now_add=True)
    lida = models.BooleanField(default=False)

    def __str__(self):
        return f"Notificação para {self.usuario.username}: {self.mensagem}"

