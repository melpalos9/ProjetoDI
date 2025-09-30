from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import (
    Conteudo, Relato, Diario, DiarioEntry, Desafio,
    RespiracaoExercise, Categoria, Perfil, Feedback
)

# -------- Inlines --------

class RelatoInline(admin.TabularInline):
    model = Relato
    extra = 1


class DiarioEntryInline(admin.TabularInline):
    model = DiarioEntry
    extra = 1


class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    extra = 0


class DiarioInline(admin.TabularInline):
    model = Diario
    extra = 1


# -------- Admins principais --------

@admin.register(Conteudo)
class ConteudoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "status", "publicado_em", "criado_em")
    search_fields = ("titulo", "resumo", "corpo")
    list_filter = ("status", "publicado_em")
    inlines = [RelatoInline]  # Relatos inline dentro de Conteúdo


@admin.register(Desafio)
class DesafioAdmin(admin.ModelAdmin):
    list_display = ("titulo", "duracao_dias", "ativo", "criado_em")
    list_filter = ("ativo",)
    inlines = [DiarioEntryInline]  # Entradas de diário inline dentro de Desafio


# Re-registra o User com Perfil + Diario inline
class UserAdmin(BaseUserAdmin):
    inlines = [PerfilInline, DiarioInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# -------- Admins simples --------

@admin.register(DiarioEntry)
class DiarioEntryAdmin(admin.ModelAdmin):
    list_display = ("titulo", "data", "humor", "tempo_total_min")
    search_fields = ("titulo", "descricao")


@admin.register(Relato)
class RelatoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "conteudo", "anonimo", "moderado", "criado_em")
    list_filter = ("anonimo", "moderado")
    search_fields = ("titulo", "relato")


@admin.register(RespiracaoExercise)
class RespiracaoExerciseAdmin(admin.ModelAdmin):
    list_display = ("titulo", "duracao_segundos", "ativo")
    list_filter = ("ativo",)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("usuario", "nota", "criado_em")
    list_filter = ("nota",)
    search_fields = ("usuario", "comentario")
