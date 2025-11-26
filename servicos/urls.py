from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_servicos, name='listar-servicos'),
    path('novo/', views.cadastrar_editar_servico, name='cadastrar-servico'),
    path('editar/<int:pk>/', views.cadastrar_editar_servico, name='editar-servico'),
    path('deletar/<int:pk>/', views.deletar_servico, name='deletar-servico'),
]