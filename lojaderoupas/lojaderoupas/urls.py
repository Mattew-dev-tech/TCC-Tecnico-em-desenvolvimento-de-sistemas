from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('contas.urls')),  # Rota principal do app

    # Reset de senha
    path('esqueci-senha/', auth_views.PasswordResetView.as_view(template_name='contas/esqueci_senha.html'), name='password_reset'),
    path('esqueci-senha/enviado/', auth_views.PasswordResetDoneView.as_view(template_name='contas/email_enviado.html'), name='password_reset_done'),
    path('redefinir-senha/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='contas/redefinir_senha.html'), name='password_reset_confirm'),
    path('redefinir-senha/concluido/', auth_views.PasswordResetCompleteView.as_view(template_name='contas/senha_alterada.html'), name='password_reset_complete'),
]

# Serve arquivos de imagem no modo DEBUG
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
