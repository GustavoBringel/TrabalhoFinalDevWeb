from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_agendamentos, name='listar-agendamentos'), # Nova listagem
    path('novo/', views.novo_editar_agendamento, name='cadastrar-agendamento'),
    path('editar/<int:pk>/', views.novo_editar_agendamento, name='editar-agendamento'),
    path('deletar/<int:pk>/', views.deletar_agendamento, name='deletar-agendamento'),
]