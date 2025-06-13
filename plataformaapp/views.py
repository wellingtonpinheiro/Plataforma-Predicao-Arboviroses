from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import joblib
import os
from django.conf import settings
from .pipeline import executar_pipeline


def carregar_modelo_casos():
    caminho_modelo = os.path.join(settings.BASE_DIR, 'meuapp', 'modelos', 'predicao_casos_2015-2016.pkl')
    modelo = joblib.load(caminho_modelo)
    return modelo

def carregar_modelo_criadouros():
    caminho_modelo = os.path.join(settings.BASE_DIR, 'meuapp', 'modelos', 'predicao_criadouros_2015-2016.pkl')
    modelo = joblib.load(caminho_modelo)
    return modelo

def fazer_predicao_casos(ano, bimestre):
    modelo = carregar_modelo_casos()
    entrada = [[int(ano), int(bimestre)]]
    resultado = modelo.predict(entrada)
    
    return resultado[0]

def fazer_predicao_criadouros(ano, bimestre):
    modelo = carregar_modelo_criadouros()
    entrada = [[int(ano), int(bimestre)]]
    resultado = modelo.predict(entrada)
    return resultado[0]

    
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
@login_required(login_url='/login/')
def casos(request):
    if request.method == 'POST':
        ano = request.POST.get('Ano')
        bimestre = request.POST.get('bimestre')

        try:
            # Predição
            resultado_predicao = fazer_predicao_casos(ano, bimestre)

            # Executar pipeline de interpolação
            sucesso, erro_pipeline = executar_pipeline('casos', ano, bimestre)
            if not sucesso:
                resultado_mapa = f"Erro ao gerar o mapa: {erro_pipeline}"
            else:
                resultado_mapa = "Mapa gerado com sucesso."

        except Exception as e:
            resultado_predicao = f"Erro na predição: {str(e)}"
            resultado_mapa = "Não foi possível gerar o mapa."

        contexto = {
            'ano': ano,
            'bimestre': bimestre,
            'resultado_predicao': resultado_predicao,
            'resultado_mapa': resultado_mapa,
            'mapa_url': f'/static/maps/mapa_{ano}_{bimestre}_casos.png'
        }
        return render(request, 'casos.html', contexto)

    return render(request, 'casos.html')

# View para a predição de criadouros
@login_required(login_url='/login/')
def criadouros(request):
    if request.method == 'POST':
        ano = request.POST.get('Ano')
        bimestre = request.POST.get('bimestre')

        try:
            # Predição
            resultado_predicao = fazer_predicao_criadouros(ano, bimestre)

            # Executar pipeline de interpolação
            sucesso, erro_pipeline = executar_pipeline('criadouros', ano, bimestre)
            if not sucesso:
                resultado_mapa = f"Erro ao gerar o mapa: {erro_pipeline}"
            else:
                resultado_mapa = "Mapa gerado com sucesso."

        except Exception as e:
            resultado_predicao = f"Erro na predição: {str(e)}"
            resultado_mapa = "Não foi possível gerar o mapa."

        contexto = {
            'ano': ano,
            'bimestre': bimestre,
            'resultado_predicao': resultado_predicao,
            'resultado_mapa': resultado_mapa,
            'mapa_url': f'/static/maps/mapa_{ano}_{bimestre}_criadouros.png'
        }
        return render(request, 'criadouros.html', contexto)

    return render(request, 'criadouros.html')
