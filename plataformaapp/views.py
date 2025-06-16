from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import joblib
import os
import json
from django.conf import settings
from .pipeline import executar_pipeline

# Caminhos dos modelos
def carregar_modelo_casos():
    caminho_modelo = os.path.join(settings.BASE_DIR, 'plataformaapp', 'modelos', 'modelo_rf_casos_2014_1.pkl')
    return joblib.load(caminho_modelo)

def carregar_modelo_criadouros():
    caminho_modelo = os.path.join(settings.BASE_DIR, 'plataformaapp', 'modelos', '')
    return joblib.load(caminho_modelo)

# Caminho JSON das métricas
CAMINHO_METRICAS_CASOS = os.path.join(settings.BASE_DIR, 'plataformaapp', 'metricas_casos (1).json')
CAMINHO_METRICAS_CRIADOUROS = os.path.join(settings.BASE_DIR, 'plataformaapp', 'metricas_criadouros.json')

# View de login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'login.html', {'error': "Usuário ou senha incorretos"})
    return render(request, 'login.html')

# View de logout
def logout_view(request):
    logout(request)
    return redirect('login')

# View da homepage
def home(request):
    return render(request, 'home.html')

# Função para carregar métricas
def carregar_metricas(tipo, ano, bimestre):
    if tipo == 'casos':
        caminho = CAMINHO_METRICAS_CASOS
        chave = f"modelo_rf_casos_{ano}_{bimestre}"
    else:
        caminho = CAMINHO_METRICAS_CRIADOUROS
        chave = f"modelo_rf_criadouros_{ano}_{bimestre}"

    try:
        with open(caminho, 'r') as f:
            metricas = json.load(f)
        valores = metricas[chave]
        return valores['corr'], valores['rmse'], valores['rrse']
    except Exception as e:
        return None, None, None

# View para predição de casos
@login_required(login_url='/login/')
def casos(request):
    contexto = {}

    if request.method == 'POST':
        ano = request.POST.get('Ano')
        bimestre = request.POST.get('bimestre')

        try:
            modelo = carregar_modelo_casos()
            entrada = [[int(ano), int(bimestre)]]
            resultado_predicao = modelo.predict(entrada)[0]

            sucesso, erro_pipeline = executar_pipeline('casos', ano, bimestre)
            if not sucesso:
                resultado_mapa = f"Erro ao gerar o mapa: {erro_pipeline}"
            else:
                resultado_mapa = "Mapa gerado com sucesso."

            coef_corr, rmse, rrse = carregar_metricas('casos', ano, bimestre)

            contexto = {
                'ano': ano,
                'bimestre': bimestre,
                'resultado_predicao': resultado_predicao,
                'resultado_mapa': resultado_mapa,
                'mapa_url': f'/static/maps/mapa_{ano}_{bimestre}_casos.png',
                'coef_corr': coef_corr,
                'rmse': rmse,
                'rrse': rrse
            }

        except Exception as e:
            contexto['erro'] = f"Erro durante a predição: {str(e)}"

    return render(request, 'casos.html', contexto)

# View para predição de criadouros
@login_required(login_url='/login/')
def criadouros(request):
    contexto = {}

    if request.method == 'POST':
        ano = request.POST.get('Ano')
        bimestre = request.POST.get('bimestre')

        try:
            modelo = carregar_modelo_criadouros()
            entrada = [[int(ano), int(bimestre)]]
            resultado_predicao = modelo.predict(entrada)[0]

            sucesso, erro_pipeline = executar_pipeline('criadouros', ano, bimestre)
            if not sucesso:
                resultado_mapa = f"Erro ao gerar o mapa: {erro_pipeline}"
            else:
                resultado_mapa = "Mapa gerado com sucesso."

            coef_corr, rmse, rrse = carregar_metricas('criadouros', ano, bimestre)

            contexto = {
                'ano': ano,
                'bimestre': bimestre,
                'resultado_predicao': resultado_predicao,
                'resultado_mapa': resultado_mapa,
                'mapa_url': f'/static/maps/mapa_{ano}_{bimestre}_criadouros.png',
                'coef_corr': coef_corr,
                'rmse': rmse,
                'rrse': rrse
            }

        except Exception as e:
            contexto['erro'] = f"Erro durante a predição: {str(e)}"

    return render(request, 'criadouros.html', contexto)
