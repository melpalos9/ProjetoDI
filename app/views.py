from django.shortcuts import render, redirect, get_object_or_404
from .models import Conteudo, Relato, Desafio, RespiracaoExercise, DiarioEntry
from django.views import View


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class ConteudosView(View):
    def get(self, request, *args, **kwargs):
        conteudos = Conteudo.objects.filter(status="published")
        return render(request, 'conteudos.html', {"conteudos": conteudos})


class RelatosView(View):
    def get(self, request, *args, **kwargs):
        relatos = Relato.objects.filter(moderado=True)
        return render(request, 'relatos.html', {"relatos": relatos})


class DesafiosView(View):
    def get(self, request, *args, **kwargs):
        desafios = Desafio.objects.filter(ativo=True)
        return render(request, 'desafios.html', {"desafios": desafios})


class RespiracaoView(View):
    def get(self, request, *args, **kwargs):
        respiracoes = RespiracaoExercise.objects.filter(ativo=True)
        return render(request, 'respiracao.html', {"respiracoes": respiracoes})


class DiarioView(View):
    def get(self, request, *args, **kwargs):
        entradas = DiarioEntry.objects.all()
        return render(request, 'diario.html', {"entradas": entradas})
from django.views.generic import DetailView
from .models import Conteudo

class ConteudoDetailView(DetailView):
    model = Conteudo
    template_name = "conteudo_detail.html"
    context_object_name = "conteudo"
from django.views import View
from django.shortcuts import render
from .models import Categoria, Perfil, Feedback


class CategoriasView(View):
    def get(self, request, *args, **kwargs):
        categorias = Categoria.objects.all()
        return render(request, "categorias.html", {"categorias": categorias})


class PerfisView(View):
    def get(self, request, *args, **kwargs):
        perfis = Perfil.objects.all()
        return render(request, "perfis.html", {"perfis": perfis})


class FeedbacksView(View):
    def get(self, request, *args, **kwargs):
        feedbacks = Feedback.objects.all()
        return render(request, "feedbacks.html", {"feedbacks": feedbacks})
from django.views import View
from django.shortcuts import render
from .models import Categoria, Perfil, Feedback


class CategoriasView(View):
    def get(self, request, *args, **kwargs):
        categorias = Categoria.objects.all()
        return render(request, "categorias.html", {"categorias": categorias})


class PerfisView(View):
    def get(self, request, *args, **kwargs):
        perfis = Perfil.objects.all()
        return render(request, "perfis.html", {"perfis": perfis})


class FeedbacksView(View):
    def get(self, request, *args, **kwargs):
        feedbacks = Feedback.objects.all()
        return render(request, "feedbacks.html", {"feedbacks": feedbacks})
from django.views.generic import DetailView
from .models import Conteudo

class ConteudoDetailView(DetailView):
    model = Conteudo
    template_name = "conteudo_detail.html"
    context_object_name = "conteudo"
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Diario
from .forms import DiarioForm

@login_required
def diario_view(request):
    diarios = Diario.objects.filter(usuario=request.user).order_by("-data")

    # Criar nova entrada
    if request.method == "POST":
        # Se for exclusão
        if "excluir_id" in request.POST:
            Diario.objects.filter(id=request.POST["excluir_id"], usuario=request.user).delete()
            return redirect("diario")

        # Se for edição
        if "editar_id" in request.POST:
            diario = Diario.objects.get(id=request.POST["editar_id"], usuario=request.user)
            diario.titulo = request.POST.get("titulo")
            diario.conteudo = request.POST.get("conteudo")
            diario.save()
            return redirect("diario")

        # Se for nova entrada
        form = DiarioForm(request.POST)
        if form.is_valid():
            novo = form.save(commit=False)
            novo.usuario = request.user
            novo.save()
            return redirect("diario")
    else:
        form = DiarioForm()

    return render(request, "diario/diario.html", {"form": form, "diarios": diarios})
