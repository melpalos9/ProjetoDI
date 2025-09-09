from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse


STATUS_CHOICES = (
    ("draft", "Rascunho"),
    ("published", "Publicado"),
)


class Conteudo(models.Model):
    titulo = models.CharField("Título", max_length=200)
    slug = models.SlugField("Slug", max_length=220, unique=True, blank=True)
    resumo = models.TextField("Resumo", blank=True)
    corpo = models.TextField("Corpo do conteúdo")
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    atualizado_em = models.DateTimeField("Atualizado em", auto_now=True)
    status = models.CharField("Status", max_length=10, choices=STATUS_CHOICES, default="draft")
    publicado_em = models.DateTimeField("Publicado em", blank=True, null=True)

    class Meta:
        ordering = ["-publicado_em", "-criado_em"]
        verbose_name = "Conteúdo"
        verbose_name_plural = "Conteúdos"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.titulo)[:200]
            slug = base
            n = 1
            while Conteudo.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        if self.status == "published" and not self.publicado_em:
            self.publicado_em = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("app:conteudo_detail", args=[self.slug])

    def __str__(self):
        return self.titulo


class DiarioEntry(models.Model):
    titulo = models.CharField("Título", max_length=200, blank=True)
    data = models.DateField("Data de registro", default=timezone.localdate)
    tempo_total_min = models.PositiveIntegerField("Tempo de uso (minutos)", default=0)
    descricao = models.TextField("Descrição/Reflexão", blank=True)
    humor = models.CharField("Humor", max_length=100, blank=True)
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)

    class Meta:
        ordering = ["-data", "-criado_em"]
        verbose_name = "Entrada de Diário"
        verbose_name_plural = "Diário"

    def __str__(self):
        return f"{self.data} — {self.titulo or 'Diário'}"


class Desafio(models.Model):
    titulo = models.CharField("Título", max_length=150)
    descricao = models.TextField("Descrição")
    duracao_dias = models.PositiveIntegerField("Duração (dias)", default=7)
    recompensa = models.CharField("Recompensa", max_length=200, blank=True)
    ativo = models.BooleanField("Ativo", default=True)
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "Desafio"
        verbose_name_plural = "Desafios"

    def __str__(self):
        return self.titulo


class RespiracaoExercise(models.Model):
    titulo = models.CharField("Título", max_length=120)
    instrucoes = models.TextField("Instruções")
    duracao_segundos = models.PositiveIntegerField("Duração (segundos)", default=60)
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    ativo = models.BooleanField("Ativo", default=True)

    class Meta:
        ordering = ["titulo"]
        verbose_name = "Exercício de Respiração"
        verbose_name_plural = "Exercícios de Respiração"

    def __str__(self):
        return self.titulo


class Relato(models.Model):
    titulo = models.CharField("Título", max_length=200, blank=True)
    relato = models.TextField("Relato")
    idade_aprox = models.PositiveIntegerField("Idade aproximada", blank=True, null=True)
    anonimo = models.BooleanField("Anônimo", default=True)
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    moderado = models.BooleanField("Aprovado pela moderação", default=False)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "Relato"
        verbose_name_plural = "Relatos"

    def __str__(self):
        return (self.titulo or f"Relato #{self.pk}")[:40]
from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    nome = models.CharField("Nome da Categoria", max_length=100, unique=True)
    descricao = models.TextField("Descrição", blank=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nome


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    pontos = models.PositiveIntegerField(default=0)
    bio = models.TextField("Biografia", blank=True)

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"

    def __str__(self):
        return self.usuario.username


class Feedback(models.Model):
    usuario = models.CharField("Usuário (opcional)", max_length=150, blank=True)
    comentario = models.TextField("Comentário")
    nota = models.PositiveIntegerField("Nota", choices=[(i, i) for i in range(1, 6)], default=5)
    criado_em = models.DateTimeField("Enviado em", auto_now_add=True)

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"

    def __str__(self):
        return f"Feedback #{self.pk} - Nota {self.nota}"
# app/models.py
from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    pontos = models.PositiveIntegerField(default=0)
    bio = models.TextField(blank=True)

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"

    def __str__(self):
        return self.usuario.username

class Feedback(models.Model):
    usuario = models.CharField("Usuário (opcional)", max_length=150, blank=True)
    comentario = models.TextField("Comentário")
    nota = models.PositiveIntegerField("Nota", choices=[(i, i) for i in range(1, 6)], default=5)
    criado_em = models.DateTimeField("Enviado em", auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"

    def __str__(self):
        return f"Feedback #{self.pk} - Nota {self.nota}"
class Conteudo(models.Model):
    titulo = models.CharField("Título", max_length=200)
    slug = models.SlugField("Slug", max_length=220, unique=True, blank=True)
    resumo = models.TextField("Resumo", blank=True)
    corpo = models.TextField("Corpo do conteúdo")
    video_url = models.URLField("Link do Vídeo (YouTube/Vimeo)", blank=True, null=True)  # 🔹 novo campo
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    atualizado_em = models.DateTimeField("Atualizado em", auto_now=True)
    status = models.CharField("Status", max_length=10, choices=STATUS_CHOICES, default="draft")
    publicado_em = models.DateTimeField("Publicado em", blank=True, null=True)
