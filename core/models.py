from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

class Animal(models.Model):
    PORTE_CHOICES = [
        ('Pequeno', 'Pequeno'),
        ('Médio', 'Médio'),
        ('Grande', 'Grande'),
    ]
    SEXO_CHOICES = [
        ('Macho', 'Macho'),
        ('Fêmea', 'Fêmea'),
    ]
    IDADE_CHOICES = [
        ('Menos de 6 meses', 'Menos de 6 meses'),
        ('7 a 11 meses', '7 a 11 meses'),
        ('1 ano', '1 ano'),
        ('2 anos', '2 anos'),
        ('3 anos', '3 anos'),
        ('4 anos', '4 anos'),
        ('5 anos', '5 anos'),
        ('6 anos', '6 anos'),
        ('7 ou mais', '7 ou mais'),
    ]
    nome = models.CharField(max_length=100)
    especie = models.CharField(max_length=50, choices=[('Cachorro', 'Cachorro'), ('Gato', 'Gato')])
    idade = models.CharField(max_length=20, choices=IDADE_CHOICES, verbose_name="Idade")
    descricao = models.TextField()
    foto = models.ImageField(upload_to='animais/')
    adotado = models.BooleanField(default=False)
    cuidador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='animais')

    porte = models.CharField(
        max_length=10,
        choices=PORTE_CHOICES,
        verbose_name="Porte",
        null=True, # Permite que animais antigos não tenham porte
        blank=True # Permite que o campo seja opcional no formulário
    )

    sexo = models.CharField(
        max_length=10,
        choices=SEXO_CHOICES,
        verbose_name="Sexo",
        null=True,
        blank=True
    )

    # Campos de contato
    whatsapp = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="WhatsApp",
        help_text="Número com DDD"
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="E-mail"
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
    titulo = models.CharField(max_length=200)
    descricao = HTMLField()
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

class AnimalFoto(models.Model):
    animal = models.ForeignKey(Animal, related_name='fotos_extras', on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='animais_extras/')

    def __str__(self):
        return f"Foto extra de {self.animal.nome}"
