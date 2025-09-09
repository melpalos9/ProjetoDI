from django.contrib import admin
from .models import (
    Conteudo, DiarioEntry, Desafio,
    RespiracaoExercise, Relato,
    Categoria, Perfil, Feedback
)


@admin.register(Conteudo)
class ConteudoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "status", "publicado_em", "criado_em")
    list_filter = ("status", "publicado_em")
    search_fields = ("titulo", "resumo", "corpo")
    prepopulated_fields = {"slug": ("titulo",)}
    ordering = ("-publicado_em",)


@admin.register(DiarioEntry)
class DiarioAdmin(admin.ModelAdmin):
    list_display = ("titulo", "data", "humor", "tempo_total_min", "criado_em")
    list_filter = ("data", "humor")
    search_fields = ("titulo", "descricao")


@admin.register(Desafio)
class DesafioAdmin(admin.ModelAdmin):
    list_display = ("titulo", "duracao_dias", "ativo", "criado_em")
    list_filter = ("ativo",)
    search_fields = ("titulo", "descricao")


@admin.register(RespiracaoExercise)
class RespiracaoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "duracao_segundos", "ativo", "criado_em")
    list_filter = ("ativo",)
    search_fields = ("titulo", "instrucoes")


@admin.register(Relato)
class RelatoAdmin(admin.ModelAdmin):
    list_display = ("__str__", "idade_aprox", "anonimo", "moderado", "criado_em")
    list_filter = ("moderado", "anonimo")
    search_fields = ("titulo", "relato")


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome", "descricao")
    search_fields = ("nome",)


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ("usuario", "pontos")
    search_fields = ("usuario__username",)
    list_filter = ("pontos",)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("__str__", "nota", "criado_em")
    list_filter = ("nota", "criado_em")
    search_fields = ("comentario", "usuario")
