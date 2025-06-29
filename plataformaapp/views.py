from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
import joblib
import os
import json
import time
from .pipeline import executar_pipeline

# === Carregamento de modelos ===
def carregar_modelo(tipo):
    nome_arquivo = f"modelo_rf_casos_2014_1.pkl"
    caminho_modelo = os.path.join(settings.BASE_DIR, 'plataformaapp', 'modelos', nome_arquivo)
    if not os.path.exists(caminho_modelo):
        raise FileNotFoundError(f"Modelo '{tipo}' não encontrado em: {caminho_modelo}")
    return joblib.load(caminho_modelo)

# === Caminhos dos arquivos de métricas ===
CAMINHO_METRICAS = {
    'casos': os.path.join(settings.BASE_DIR, 'plataformaapp', 'metricas_casos.json'),
    'criadouros': os.path.join(settings.BASE_DIR, 'plataformaapp', 'metricas_criadouros.json')
}

# === Função para carregar métricas ===
def carregar_metricas(tipo, ano, bimestre):
    try:
        chave = f"modelo_rf_{tipo}_{ano}_{int(bimestre):02d}"
        caminho = CAMINHO_METRICAS[tipo]

        if not os.path.exists(caminho):
            raise FileNotFoundError(f"Arquivo de métricas não encontrado: {caminho}")

        with open(caminho, 'r') as f:
            metricas = json.load(f)

        if chave not in metricas:
            raise KeyError(f"Chave {chave} não encontrada no arquivo de métricas")

        valores = metricas[chave]
        return valores.get('corr'), valores.get('rmse'), valores.get('rrse')
    except Exception as e:
        print(f"[ERRO] ao carregar métricas: {str(e)}")
        return None, None, None

# === View de login ===
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error': "Usuário ou senha incorretos"})
    return render(request, 'login.html')

# === View de logout ===
def logout_view(request):
    logout(request)
    return redirect('login')

# === View da home ===
def home(request):
    return render(request, 'home.html')

# === View genérica para 'casos' e 'criadouros' ===
def view_predicao(request, tipo):
    contexto = {
        'metricas_disponiveis': False,
        'mapa_interativo': True
    }

    BIMESTRE_MAP = {
        'jan-fev': 1,
        'mar-abr': 2,
        'mai-jun': 3,
        'jul-ago': 4,
        'set-out': 5,
        'nov-dez': 6
    }

    if request.method == 'POST':
        ano = request.POST.get('Ano')
        bimestre_nome = request.POST.get('bimestre')
        bimestre = BIMESTRE_MAP.get(bimestre_nome)

        if not ano or not bimestre:
            contexto['erro'] = "Ano ou bimestre não foram selecionados corretamente."
            return render(request, f'{tipo}.html', contexto)

        try:
            modelo = carregar_modelo(tipo)

            import pandas as pd
            nome_arquivo_csv = f'ConjuntoPredicaoArboviroses_{ano}_{int(bimestre):02d}.csv'

          
            # === Leitura para predição ===
            caminho_csv = os.path.join(settings.BASE_DIR, 'INTERPOLAÇÃO', 'conjunto treino casos', nome_arquivo_csv)
            if not os.path.exists(caminho_csv):
                raise FileNotFoundError(f"Arquivo CSV para predição não encontrado: {caminho_csv}")

            df = pd.read_csv(caminho_csv)
            if 'predicao' in df.columns:
                df = df.drop(columns=['predicao'])

            feature_names = [
                'latitude', 'longitude',
                'cb1', 't1b1', 't2b1', 'p1b1', 'p2b1', 'v1b1', 'v2b1', 'ur1b1', 'ur2b1',
                'cb2', 't1b2', 't2b2', 'p1b2', 'p2b2', 'v1b2', 'v2b2', 'ur1b2', 'ur2b2',
                'cb3', 't1b3', 't2b3', 'p1b3', 'p2b3', 'v1b3', 'v2b3', 'ur1b3', 'ur2b3',
                'cb4', 't1b4', 't2b4', 'p1b4', 'p2b4', 'v1b4', 'v2b4', 'ur1b4', 'ur2b4',
                'cb5', 't1b5', 't2b5', 'p1b5', 'p2b5', 'v1b5', 'v2b5', 'ur1b5', 'ur2b5',
                'cb6', 't1b6', 't2b6', 'p1b6', 'p2b6', 'v1b6', 'v2b6', 'ur1b6', 'ur2b6'
            ]
            df = df[feature_names]

            _ = modelo.predict(df)

            sucesso, erro_pipeline = executar_pipeline(tipo, ano, bimestre)
            coef_corr, rmse, rrse = carregar_metricas(tipo, ano, bimestre)

            nome_base = f'mapa_{ano}_{int(bimestre):02d}_{tipo}'
            tif_path = os.path.join(settings.BASE_DIR, 'static', 'maps', 'predicao_recife.tif')
            tif_url = f'/static/maps/predicao_recife.tif'
            png_path = os.path.join(settings.BASE_DIR, 'plataformaapp', 'static', 'maps', 'predicao_recife.png')
            png_existe = os.path.isfile(png_path)
            png_url = f'/static/maps/predicao_recife.png'
            geojson_path = os.path.join(settings.BASE_DIR, 'static', 'maps', f'{nome_base}.geojson')
            geojson_url = f'/static/maps/{nome_base}.geojson'

            contexto.update({
                'ano': ano,
                'bimestre': bimestre_nome,
                'resultado_mapa': "Dados prontos para o mapa." if sucesso else f"Erro: {erro_pipeline}",
                'tif_url': tif_url,
                'geojson_url': geojson_url,
                'png_url': png_url,
                'coef_corr': coef_corr,
                'rmse': rmse,
                'rrse': rrse,
                'metricas_disponiveis': all(v is not None for v in [coef_corr, rmse, rrse]),
                'mapa_disponivel': True,
                'debug_info': {
                    'tif_path': tif_path,
                    'png_path': png_path,
                    'geojson_path': geojson_path,
                    'metricas_chave': f"modelo_rf_{tipo}_{ano}_{int(bimestre):02d}",
                    'timestamp': int(time.time())
                }
            })

        except Exception as e:
            contexto['erro'] = f"Erro durante a predição: {str(e)}"
            print(f"[ERRO] View {tipo}: {str(e)}")

    return render(request, f'{tipo}.html', contexto)

# === Views específicas que usam a genérica ===
@login_required(login_url='/login/')
def casos(request):
    return view_predicao(request, 'casos')

@login_required(login_url='/login/')
def criadouros(request):
    return view_predicao(request, 'criadouros')

# === Teste da pipeline ===
def executar_teste_pipeline(request):
    tipo = 'casos'
    ano = 2014
    bimestre = 1

    sucesso, erro_pipeline = executar_pipeline(tipo, ano, bimestre)
    coef_corr, rmse, rrse = carregar_metricas(tipo, ano, bimestre)

    tif_path = os.path.join(settings.BASE_DIR, 'static', 'maps', 'predicao_recife.tif')
    tif_url = f'/static/maps/predicao_recife.tif?v={int(time.time())}'

    contexto = {
        'mensagem': 'Pipeline executada com sucesso!' if sucesso else f'Erro: {erro_pipeline}',
        'tif_url': tif_url,
        'coef_corr': coef_corr,
        'rmse': rmse,
        'rrse': rrse,
        'ano': ano,
        'bimestre': bimestre,
        'metricas_disponiveis': all(v is not None for v in [coef_corr, rmse, rrse]),
        'mapa_disponivel': os.path.exists(tif_path),
        'mapa_interativo': True
    }

    return render(request, 'home.html', contexto)