from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

from . forms import CustomUserCreationForm


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

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirecionar para a página de login após o logout

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
