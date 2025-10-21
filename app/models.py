from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# -----------------------------
# STATUS PADRÃO
# -----------------------------
STATUS_CHOICES = (
    ("draft", "Rascunho"),
    ("published", "Publicado"),
)


# -----------------------------
# CATEGORIAS
# -----------------------------
class Categoria(models.Model):
    nome = models.CharField("Nome da Categoria", max_length=100, unique=True)
    descricao = models.TextField("Descrição", blank=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nome


# -----------------------------
# CONTEÚDOS
# -----------------------------
class Conteudo(models.Model):
    titulo = models.CharField("Título", max_length=200)
    slug = models.SlugField("Slug", max_length=220, unique=True, blank=True)
    resumo = models.TextField("Resumo", blank=True)
    corpo = models.TextField("Corpo do conteúdo")
    video_url = models.URLField("Link do Vídeo (YouTube/Vimeo)", blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Categoria")
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
        return reverse("conteudo_detail", args=[self.slug])

    def __str__(self):
        return self.titulo


# -----------------------------
# PERFIL
# -----------------------------
class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    pontos = models.PositiveIntegerField(default=0)
    bio = models.TextField("Biografia", blank=True)
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"

    def __str__(self):
        return self.usuario.username


# 🔹 Cria automaticamente um Perfil para cada novo usuário
@receiver(post_save, sender=User)
def criar_perfil_automaticamente(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(usuario=instance)


# -----------------------------
# DIÁRIO
# -----------------------------
class Diario(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name="diarios")
    titulo = models.CharField("Título", max_length=200)
    conteudo = models.TextField("Conteúdo")
    data = models.DateTimeField("Data", default=timezone.now)
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)

    class Meta:
        ordering = ["-data"]
        verbose_name = "Entrada de Diário"
        verbose_name_plural = "Diário"

    def __str__(self):
        return f"{self.perfil.usuario.username} - {self.titulo}"


# -----------------------------
# DESAFIOS
# -----------------------------
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


# -----------------------------
# RELATOS
# -----------------------------
class Relato(models.Model):
    conteudo = models.ForeignKey(Conteudo, on_delete=models.CASCADE, related_name="relatos")
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


# -----------------------------
# RESPIRAÇÃO
# -----------------------------
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


# -----------------------------
# FEEDBACKS
# -----------------------------
class Feedback(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name="feedbacks", null=True, blank=True)
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