from django.contrib import admin
from django.urls import path
from app.views import (
    IndexView, ConteudosView, RelatosView,
    DesafiosView, RespiracaoView, DiarioView,
    ConteudoDetailView, CategoriasView, PerfisView, FeedbacksView
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", IndexView.as_view(), name="index"),  # 👈 ESTA LINHA FALTANDO
    path("conteudos/", ConteudosView.as_view(), name="conteudos"),
    path("conteudo/<slug:slug>/", ConteudoDetailView.as_view(), name="conteudo_detail"),
    path("relatos/", RelatosView.as_view(), name="relatos"),
    path("desafios/", DesafiosView.as_view(), name="desafios"),
    path("respiracao/", RespiracaoView.as_view(), name="respiracao"),
    path("diario/", DiarioView.as_view(), name="diario"),
    path("categorias/", CategoriasView.as_view(), name="categorias"),
    path("perfis/", PerfisView.as_view(), name="perfis"),
    path("feedbacks/", FeedbacksView.as_view(), name="feedbacks"),
]
