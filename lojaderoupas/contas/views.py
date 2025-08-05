from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
print("views.py carregando")
from .models import Roupa
from .forms import RoupaForm
from .forms import PedidoForm
from .forms import ItemPedidoFormSet
from .models import Pedido, ItemPedido
from django.shortcuts import get_object_or_404, redirect

@login_required
def fazer_pedido(request):
    if request.method == 'POST':
        formset = ItemPedidoFormSet(request.POST, usuario=request.user)
        if formset.is_valid():
            pedido = Pedido.objects.create(usuario=request.user)
            for form in formset:
                # Só salva se o formulário tiver dados válidos preenchidos
                if form.cleaned_data:
                    roupa = form.cleaned_data['roupa']
                    quantidade = form.cleaned_data['quantidade']
                    ItemPedido.objects.create(pedido=pedido, roupa=roupa, quantidade=quantidade)
            return redirect('ver_pedidos')
    else:
        formset = ItemPedidoFormSet(usuario=request.user)

    return render(request, 'contas/fazer_pedido.html', {'formset': formset})

@login_required
def editar_roupa_view(request, id):
    roupa = get_object_or_404(Roupa, id=id, usuario=request.user)
    if request.method == 'POST':
        form = RoupaForm(request.POST, request.FILES, instance=roupa)
        if form.is_valid():
            form.save()
            return redirect('ver_roupas')
    else:
        form = RoupaForm(instance=roupa)
    return render(request, 'contas/editar_roupa.html', {'form': form})

@login_required
def excluir_roupa_view(request, id):
    roupa = get_object_or_404(Roupa, id=id, usuario=request.user)
    roupa.delete()
    return redirect('ver_roupas')

@login_required
def cadastrar_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.usuario = request.user
            pedido.save()
            return redirect('ver_pedidos')
    else:
        form = PedidoForm()
    return render(request, 'contas/cadastro_pedido.html', {'form': form})

@login_required
def lista_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user)
    return render(request, 'lista_pedidos.html', {'pedidos': pedidos})

class MinhaPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'contas/password_reset_confirm.html'
    success_url = reverse_lazy('senha_redefinida')

class MinhaPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'contas/password_reset_complete.html'

class MinhaPasswordResetView(PasswordResetView):
    template_name = 'contas/esqueceu_senha.html'  # <-- nome correto do formulário
    email_template_name = 'contas/email_reset.html'
    success_url = reverse_lazy('email_enviado')

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        users = User.objects.filter(email=email)
        if users.exists():
            user = users[0]
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            link = f"http://127.0.0.1:8000/redefinir-senha/{uid}/{token}/"
            self.extra_context = {"reset_link": link}
        return super().form_valid(form)

def redefinir_senha(request, token):
    if request.method == 'POST':
        nova_senha = request.POST.get('nova_senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if nova_senha != confirmar_senha:
            messages.error(request, 'As senhas não coincidem.')
            return render(request, 'contas/redefinir_senha.html')

        user_id = request.session.get('user_id')
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                user.password = make_password(nova_senha)
                user.save()
                return redirect('senha_alterada')
            except User.DoesNotExist:
                messages.error(request, 'Usuário não encontrado.')
        else:
            messages.error(request, 'Token inválido ou expirado.')

    return render(request, 'contas/redefinir_senha.html')

def esqueceu_senha(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            token = get_random_string(20)
            # Aqui você pode salvar o token em um modelo ou session
            link = f"http://127.0.0.1:8000/redefinir-senha/{token}"

            send_mail(
                'Recuperação de senha',
                f'Olá, clique no link para redefinir sua senha: {link}',
                'seuemail@gmail.com',
                [email],
                fail_silently=False,
            )
        except User.DoesNotExist:
            pass  # Não mostra erro para proteger dados

        return redirect('email_enviado')

    return render(request, 'contas/esqueceu_senha.html')

@login_required(login_url='login')
def painel_view(request):
    return render(request, 'contas/painel.html', {'usuario': request.user})

@login_required
def cadastrar_roupa(request):
    if request.method == 'POST':
        form = RoupaForm(request.POST, request.FILES)
        if form.is_valid():
            roupa = form.save(commit=False)
            roupa.usuario = request.user
            roupa.save()
            return redirect('ver_roupas')
    else:
        form = RoupaForm()
    return render(request, 'contas/cadastro_roupa.html', {'form': form})

@login_required
def ver_roupas_view(request):
    roupas = Roupa.objects.filter(usuario=request.user)
    return render(request, 'contas/ver_roupas.html', {'roupas': roupas})

@login_required
def ver_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user)
    return render(request, 'contas/ver_pedidos.html', {'pedidos': pedidos})

def logout_view(request):
    logout(request)
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('painel')  # ou painel depois
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
    return render(request, 'contas/login.html')

def cadastro_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, 'As senhas não coincidem.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Esse nome de usuário já existe.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Esse e-mail já está em uso.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, 'Cadastro realizado com sucesso! Faça o login.')
            return redirect('login')

    return render(request, 'contas/cadastro.html')

def email_enviado(request):
    return render(request, 'contas/email_enviado.html')

def senha_alterada(request):
    return render(request, 'contas/senha_alterada.html')

