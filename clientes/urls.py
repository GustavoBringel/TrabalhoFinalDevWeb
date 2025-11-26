from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_clientes, name='listar-clientes'), # Nova listagem
    path('novo/', views.cadastrar_editar_cliente, name='cadastrar-cliente'),
    path('editar/<int:pk>/', views.cadastrar_editar_cliente, name='editar-cliente'),
    path('deletar/<int:pk>/', views.deletar_cliente, name='deletar-cliente'),
]
