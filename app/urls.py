from django.urls import path
from . import views

app_name = "app"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("conteudos/", views.ConteudosView.as_view(), name="conteudos"),
    path("conteudo/<slug:slug>/", views.ConteudoDetailView.as_view(), name="conteudo_detail"),  # CORRIGIDO
    path("relatos/", views.RelatosView.as_view(), name="relatos"),
    path("desafios/", views.DesafiosView.as_view(), name="desafios"),
    path("respiracao/", views.RespiracaoView.as_view(), name="respiracao"),
    path("categorias/", views.CategoriasView.as_view(), name="categorias"),
    path("perfis/", views.PerfisView.as_view(), name="perfis"),
    path("feedbacks/", views.FeedbacksView.as_view(), name="feedbacks"),
    path("diario/", views.DiarioView.as_view(), name="diario"),
]