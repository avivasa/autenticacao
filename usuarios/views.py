# Create your views here.
from django.shortcuts import render, redirect
# função utilizada na view de login
from django.contrib.auth import authenticate
# função utilizada na view de login
from django.contrib.auth import login
# função utilizada para logout 
from django.contrib.auth import logout


# Utilizado na Função de Registro 
from django.contrib.auth.forms import UserCreationForm

# Alteração da Senha
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


# reset passowrd
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes

# reset senha via e-mail 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import send_mail


# password reset confirm
try:
    from django.utils.encoding import force_text
except:
    from django.utils.encoding import force_str as force_text
from django.contrib.auth.forms import SetPasswordForm


from django.contrib.auth import get_user_model



from django.urls import reverse


from . forms import CustomUserCreationForm

from .models import CustomUser

# Função de autenticação do Django 
# função de login 
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirecionar para a página principal após o login
        else:
            # Exibir uma mensagem de erro
            return render(request, 'login.html', {'error_message': 'Credenciais inválidas.'})
    return render(request, 'login.html')

# função para realizar logout
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirecionar para a página de login após o logout

# função para registrar 
def register_view(request):
    if request.method == 'POST':
        #form = UserCreationForm(request.POST)
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirecionar para a página de login 
    else:
        #form = UserCreationForm()
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Atualiza a sessão do usuário, 
            return redirect('home')  # Redirecionar para a página principal
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})

# resetar a senha
def password_reset_request(request):
    if request.method == "POST":
        email = request.POST['email']
        associated_users = CustomUser.objects.filter(email=email)
        if associated_users.exists():
            for user in associated_users:
                subject = "Redefinição de Senha"
                email_template_name = "password_reset_email.txt"
                c = {
                    "email": user.email,
                    'domain': 'example.com',  # Troque isso pelo seu domínio
                    'site_name': 'SeuSite',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',  # Altere para 'https' se estiver usando HTTPS
                }
                email = render_to_string(email_template_name, c)
                send_mail(subject, email, 'youremail@example.com', [user.email], fail_silently=False)
            return redirect("/usuarios/password_reset/done/")
    return render(request, "password_reset.html")

def password_reset_confirm(request, uidb64, token):
    # Implemente a lógica para redefinir a senha com base no uidb64 e token fornecidos
    return render(request, "password_reset_confirm.html")

def password_reset_done(request):
    # Implemente a lógica para redefinir a senha com base no uidb64 e token fornecidos
    return render(request, "password_reset_done.html")    

def password_reset_complete(request):
    # Implemente a lógica para redefinir a senha com base no uidb64 e token fornecidos
    return render(request, "password_reset_complete.html")  


def password_reset_confirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('password_reset_complete')
        else:
            form = SetPasswordForm(user)
        return render(request, 'password_reset_confirm.html', {'form': form})
    else:
        return render(request, 'password_reset_invalid.html')

def password_reset_confirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('password_reset_complete')  # Corrigido aqui
        else:
            form = SetPasswordForm(user)
        return render(request, 'password_reset_confirm.html', {'form': form})
    else:
        return render(request, 'password_reset_invalid.html')