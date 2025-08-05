from django.urls import path
from . import views
from .views import ver_roupas_view
from .views import editar_roupa_view, excluir_roupa_view
from .views import (
    MinhaPasswordResetView,
    MinhaPasswordResetConfirmView,
    MinhaPasswordResetCompleteView,
    email_enviado,
)

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('painel/', views.painel_view, name='painel'),

    # reset de senha
    path('esqueceu-senha/', MinhaPasswordResetView.as_view(), name='esqueceu_senha'),
    path('email-enviado/', email_enviado, name='email_enviado'),
    path('redefinir-senha/<uidb64>/<token>/', views.redefinir_senha, name='redefinir_senha'),
    path('senha-alterada/', views.senha_alterada, name='senha_alterada'),
    path('reset/<uidb64>/<token>/', MinhaPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/sucesso/', MinhaPasswordResetCompleteView.as_view(), name='senha_redefinida'),

    # roupas
    path('cadastrar-roupa/', views.cadastrar_roupa, name='cadastrar_roupa'),
    path('ver-roupas/', ver_roupas_view, name='ver_roupas'),
    path('ver-pedidos/', views.ver_pedidos, name='ver_pedidos'),
    
    # pedidos
    path('cadastrar-pedido/', views.cadastrar_pedido, name='cadastro_pedido'),
    path('pedidos/', views.lista_pedidos, name='lista_pedidos'),
    path('fazer-pedido/', views.fazer_pedido, name='fazer_pedido'),

     # ... Para excluir  ...
    path('editar-roupa/<int:id>/', editar_roupa_view, name='editar_roupa'),
    path('excluir-roupa/<int:id>/', excluir_roupa_view, name='excluir_roupa'),
]

