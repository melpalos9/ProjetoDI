from django.contrib import admin
from .models import (
    Conteudo, Relato, Desafio, Diario,
    RespiracaoExercise, Categoria, Perfil, Feedback
)


# ---------------------------
# INLINES
# ---------------------------

class RelatoInline(admin.TabularInline):
    model = Relato
    extra = 1
    fields = ("titulo", "relato", "idade_aprox", "anonimo", "moderado", "criado_em")
    readonly_fields = ("criado_em",)
    show_change_link = True


class DiarioInline(admin.TabularInline):
    model = Diario
    extra = 1
    fields = ("titulo", "conteudo", "data", "criado_em")
    readonly_fields = ("data", "criado_em")


class FeedbackInline(admin.TabularInline):
    model = Feedback
    extra = 1
    fields = ("usuario", "comentario", "nota", "criado_em")
    readonly_fields = ("criado_em",)


# ---------------------------
# ADMIN PRINCIPAIS
# ---------------------------

@admin.register(Conteudo)
class ConteudoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "categoria", "status", "publicado_em", "criado_em")
    list_filter = ("status", "categoria")
    search_fields = ("titulo", "resumo", "corpo")
    prepopulated_fields = {"slug": ("titulo",)}
    inlines = [RelatoInline]


@admin.register(Desafio)
class DesafioAdmin(admin.ModelAdmin):
    list_display = ("titulo", "duracao_dias", "ativo", "criado_em")
    list_filter = ("ativo",)
    search_fields = ("titulo", "descricao")


@admin.register(RespiracaoExercise)
class RespiracaoExerciseAdmin(admin.ModelAdmin):
    list_display = ("titulo", "duracao_segundos", "ativo", "criado_em")
    list_filter = ("ativo",)
    search_fields = ("titulo", "instrucoes")


@admin.register(Diario)
class DiarioAdmin(admin.ModelAdmin):
    list_display = ("perfil", "titulo", "data")
    search_fields = ("perfil__usuario__username", "titulo", "conteudo")
    list_filter = ("data",)
    autocomplete_fields = ("perfil",)


@admin.register(Relato)
class RelatoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "anonimo", "moderado", "criado_em")
    list_filter = ("moderado", "anonimo")
    search_fields = ("titulo", "relato")


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ("usuario", "pontos", "criado_em")
    search_fields = ("usuario__username",)
    list_filter = ("pontos",)
    inlines = [DiarioInline, FeedbackInline]


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("usuario", "nota", "criado_em")
    list_filter = ("nota",)
    search_fields = ("usuario", "comentario")