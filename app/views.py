from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.contrib import messages
from .models import Conteudo, Perfil, Feedback, Diario, Categoria, Relato, Desafio, RespiracaoExercise
from .forms import DiarioForm, FeedbackForm


# -----------------------
# PÁGINA INICIAL
# -----------------------
class IndexView(View):
    def get(self, request):
        # Estatísticas para a página inicial
        estatisticas = {
            'total_conteudos': Conteudo.objects.filter(status="published").count(),
            'total_usuarios': Perfil.objects.count(),
            'total_feedbacks': Feedback.objects.count(),
            'total_diarios': Diario.objects.count(),
        }
        
        # Conteúdos recentes para exibir na homepage
        conteudos_recentes = Conteudo.objects.filter(status="published").order_by('-publicado_em')[:3]
        
        context = {
            'estatisticas': estatisticas,
            'conteudos_recentes': conteudos_recentes,
        }
        
        return render(request, "index.html", context)


# -----------------------
# CONTEÚDOS
# -----------------------
class ConteudosView(View):
    def get(self, request):
        conteudos = Conteudo.objects.filter(status="published").order_by("-publicado_em")
        
        # Filtro por categoria se fornecido
        categoria_id = request.GET.get('categoria')
        if categoria_id:
            conteudos = conteudos.filter(categoria_id=categoria_id)
        
        categorias = Categoria.objects.all()
        
        context = {
            "conteudos": conteudos,
            "categorias": categorias,
            "categoria_selecionada": int(categoria_id) if categoria_id else None,
        }
        return render(request, "conteudos.html", context)


class ConteudoDetailView(View):
    def get(self, request, slug):
        conteudo = get_object_or_404(Conteudo, slug=slug, status="published")
        
        # Relatos aprovados relacionados a este conteúdo
        relatos = conteudo.relatos.filter(moderado=True)
        
        # Conteúdos relacionados (mesma categoria)
        conteudos_relacionados = Conteudo.objects.filter(
            status="published",
            categoria=conteudo.categoria
        ).exclude(id=conteudo.id).order_by('-publicado_em')[:3]
        
        context = {
            "conteudo": conteudo,
            "relatos": relatos,
            "conteudos_relacionados": conteudos_relacionados,
        }
        return render(request, "conteudo_detail.html", context)


# -----------------------
# RELATOS
# -----------------------
class RelatosView(View):
    def get(self, request):
        relatos = Relato.objects.filter(moderado=True).order_by("-criado_em")
        
        # Estatísticas dos relatos
        total_relatos = relatos.count()
        relatos_anonimos = relatos.filter(anonimo=True).count()
        
        context = {
            "relatos": relatos,
            "total_relatos": total_relatos,
            "relatos_anonimos": relatos_anonimos,
        }
        return render(request, "relatos.html", context)


# -----------------------
# DESAFIOS
# -----------------------
class DesafiosView(View):
    def get(self, request):
        desafios = Desafio.objects.filter(ativo=True).order_by("-criado_em")
        
        # Desafio em destaque (mais recente)
        desafio_destaque = desafios.first() if desafios.exists() else None
        
        context = {
            "desafios": desafios,
            "desafio_destaque": desafio_destaque,
        }
        return render(request, "desafios.html", context)


# -----------------------
# RESPIRAÇÃO
# -----------------------
class RespiracaoView(View):
    def get(self, request):
        exercicios = RespiracaoExercise.objects.filter(ativo=True).order_by("titulo")
        
        # Exercícios por duração
        exercicios_rapidos = exercicios.filter(duracao_segundos__lte=60)
        exercicios_medios = exercicios.filter(duracao_segundos__gt=60, duracao_segundos__lte=180)
        exercicios_longos = exercicios.filter(duracao_segundos__gt=180)
        
        context = {
            "exercicios": exercicios,
            "exercicios_rapidos": exercicios_rapidos,
            "exercicios_medios": exercicios_medios,
            "exercicios_longos": exercicios_longos,
        }
        return render(request, "respiracao.html", context)


# -----------------------
# CATEGORIAS
# -----------------------
class CategoriasView(View):
    def get(self, request):
        categorias = Categoria.objects.all()
        
        # Contar conteúdos por categoria
        categorias_com_contagem = []
        for categoria in categorias:
            count = Conteudo.objects.filter(categoria=categoria, status="published").count()
            categorias_com_contagem.append({
                'categoria': categoria,
                'quantidade': count
            })
        
        context = {
            "categorias_com_contagem": categorias_com_contagem,
        }
        return render(request, "categorias.html", context)


# -----------------------
# PERFIS - CORRIGIDA
# -----------------------
class PerfisView(View):
    def get(self, request):
        perfis = Perfil.objects.all().order_by('-pontos')
        
        # CORREÇÃO: Calcular média de pontos de forma segura
        resultado_agregacao = perfis.aggregate(media_pontos=models.Avg('pontos'))
        media_pontos = resultado_agregacao['media_pontos'] or 0
        
        # Estatísticas para o template
        context = {
            'perfis': perfis,
            'top_pontuacao': perfis.first() if perfis.exists() else None,
            'media_pontos': round(media_pontos, 1),
            'diarios_count': Diario.objects.count(),
        }
        
        return render(request, "perfis.html", context)


# -----------------------
# FEEDBACKS - CORRIGIDA
# -----------------------
class FeedbacksView(View):
    def get(self, request):
        form = FeedbackForm()
        feedbacks = Feedback.objects.order_by("-criado_em")
        
        # CORREÇÃO: Calcular média de notas de forma segura
        resultado_agregacao = feedbacks.aggregate(media_notas=models.Avg('nota'))
        media_notas = resultado_agregacao['media_notas'] or 0
        
        # Estatísticas dos feedbacks
        total_feedbacks = feedbacks.count()
        
        context = {
            "form": form, 
            "feedbacks": feedbacks,
            "total_feedbacks": total_feedbacks,
            "media_notas": round(media_notas, 1),
        }
        return render(request, "feedbacks.html", context)

    def post(self, request):
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            if request.user.is_authenticated:
                try:
                    perfil = Perfil.objects.get(usuario=request.user)
                    feedback.perfil = perfil
                    feedback.usuario = request.user.username
                except Perfil.DoesNotExist:
                    feedback.usuario = "Usuário Anônimo"
            else:
                feedback.usuario = "Visitante"
            
            feedback.save()
            messages.success(request, "Obrigado pelo seu feedback! 💖")
            return redirect("app:feedbacks")
        
        # Se o formulário for inválido, recarrega a página com erros
        feedbacks = Feedback.objects.order_by("-criado_em")
        
        # CORREÇÃO: Calcular média de forma segura
        resultado_agregacao = feedbacks.aggregate(media_notas=models.Avg('nota'))
        media_notas = resultado_agregacao['media_notas'] or 0
        
        context = {
            "form": form, 
            "feedbacks": feedbacks,
            "total_feedbacks": feedbacks.count(),
            "media_notas": round(media_notas, 1),
        }
        return render(request, "feedbacks.html", context)


# -----------------------
# DIÁRIO (Requer login)
# -----------------------
class DiarioView(LoginRequiredMixin, View):
    login_url = '/admin/login/'  # Redireciona para login se não autenticado
    
    def get(self, request):
        form = DiarioForm()
        try:
            perfil = Perfil.objects.get(usuario=request.user)
            diarios = Diario.objects.filter(perfil=perfil).order_by("-data")
            
            # Estatísticas do diário do usuário
            total_entradas = diarios.count()
            entrada_recente = diarios.first() if diarios.exists() else None
            
        except Perfil.DoesNotExist:
            diarios = []
            total_entradas = 0
            entrada_recente = None
        
        context = {
            "form": form, 
            "diarios": diarios,
            "total_entradas": total_entradas,
            "entrada_recente": entrada_recente,
        }
        return render(request, "diario.html", context)

    def post(self, request):
        try:
            perfil = Perfil.objects.get(usuario=request.user)
        except Perfil.DoesNotExist:
            messages.error(request, "Perfil não encontrado.")
            return redirect("app:diario")

        # Excluir entrada
        if "excluir_id" in request.POST:
            try:
                diario = Diario.objects.get(id=request.POST["excluir_id"], perfil=perfil)
                diario.delete()
                messages.success(request, "Entrada do diário excluída com sucesso. 🗑️")
            except Diario.DoesNotExist:
                messages.error(request, "Entrada não encontrada.")
            return redirect("app:diario")

        # Editar entrada
        if "editar_id" in request.POST:
            try:
                diario = Diario.objects.get(id=request.POST["editar_id"], perfil=perfil)
                diario.titulo = request.POST.get("titulo")
                diario.conteudo = request.POST.get("conteudo")
                diario.save()
                messages.success(request, "Entrada atualizada com sucesso! ✏️")
            except Diario.DoesNotExist:
                messages.error(request, "Entrada não encontrada.")
            return redirect("app:diario")

        # Nova entrada
        form = DiarioForm(request.POST)
        if form.is_valid():
            novo = form.save(commit=False)
            novo.perfil = perfil
            novo.save()
            
            # Adiciona pontos por nova entrada
            perfil.pontos += 10
            perfil.save()
            
            messages.success(request, "Entrada adicionada ao diário! +10 pontos 🎉")
            return redirect("app:diario")
        else:
            messages.error(request, "Erro ao salvar a entrada. Verifique os dados.")

        # Recarrega a página se houver erro
        diarios = Diario.objects.filter(perfil=perfil).order_by("-data")
        context = {
            "form": form, 
            "diarios": diarios,
            "total_entradas": diarios.count(),
            "entrada_recente": diarios.first() if diarios.exists() else None,
        }
        return render(request, "diario.html", context)


# -----------------------
# VIEWS ADICIONAIS
# -----------------------

class SobreView(View):
    """Página sobre o projeto"""
    def get(self, request):
        return render(request, "sobre.html")


class ContatoView(View):
    """Página de contato"""
    def get(self, request):
        return render(request, "contato.html")


class EstatisticasView(View):
    """Página de estatísticas da plataforma"""
    def get(self, request):
        # CORREÇÃO: Todas as agregações de forma segura
        estatisticas_agregadas = Perfil.objects.aggregate(
            total_pontos=models.Sum('pontos'),
            total_usuarios=models.Count('id')
        )
        
        estatisticas = {
            # Usuários
            'total_usuarios': estatisticas_agregadas['total_usuarios'] or 0,
            'usuarios_ativos': Perfil.objects.filter(diarios__isnull=False).distinct().count(),
            'pontuacao_total': estatisticas_agregadas['total_pontos'] or 0,
            
            # Conteúdo
            'total_conteudos': Conteudo.objects.filter(status="published").count(),
            'total_relatos': Relato.objects.filter(moderado=True).count(),
            'total_desafios': Desafio.objects.filter(ativo=True).count(),
            'total_exercicios': RespiracaoExercise.objects.filter(ativo=True).count(),
            
            # Interações
            'total_diarios': Diario.objects.count(),
            'total_feedbacks': Feedback.objects.count(),
        }
        
        # CORREÇÃO: Média de notas de forma segura
        media_notas_agregada = Feedback.objects.aggregate(media=models.Avg('nota'))
        estatisticas['media_notas'] = round(media_notas_agregada['media'] or 0, 1)
        
        # Top 5 usuários
        top_usuarios = Perfil.objects.all().order_by('-pontos')[:5]
        
        # Conteúdos mais recentes
        conteudos_recentes = Conteudo.objects.filter(status="published").order_by('-publicado_em')[:5]
        
        context = {
            'estatisticas': estatisticas,
            'top_usuarios': top_usuarios,
            'conteudos_recentes': conteudos_recentes,
        }
        
        return render(request, "estatisticas.html", context)


# -----------------------
# VIEWS DE API SIMPLES
# -----------------------

class APIConteudosView(View):
    """API simples para listar conteúdos (JSON)"""
    def get(self, request):
        conteudos = Conteudo.objects.filter(status="published").values(
            'id', 'titulo', 'slug', 'resumo', 'publicado_em'
        )
        from django.http import JsonResponse
        return JsonResponse(list(conteudos), safe=False)


class APIPerfisView(View):
    """API simples para listar perfis (JSON)"""
    def get(self, request):
        perfis = Perfil.objects.all().values(
            'usuario__username', 'pontos', 'bio', 'criado_em'
        )
        from django.http import JsonResponse
        return JsonResponse(list(perfis), safe=False)