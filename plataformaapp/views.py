from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


# View para a pagina de login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            error_message = "Usuário ou senha incorretos"
            return render(request, 'login.html', {'error': error_message})
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

# View para a homepage
def home(request):
    return render(request, 'home.html')

# View para a predição de casos
@login_required(login_url='/login/')  #somente usuarios logados podem acessar
def casos(request):
    return render(request, 'casos.html')

# View para a predição de criadouros
@login_required(login_url='/login/')  #somente usuarios logados podem acessar

def criadouros(request):
    return render(request, 'criadouros.html')
