"""
Código para a organização dos dados do INMET. Os dados são organizados por ano, por mês e por bairro

Criado por: Equipe de Geo-saúde do grupo de Computação Biomédica (DEBM-UFPE)
Data: 30/04/2022
Última atualização: 10/11/2023
contatos: cll@ecomp.poli.br, acgs@ecomp.poli.br, wellington.santos@ufpe.br
"""

import extract_zipped_files
import processINMETdata
import pandas as pd
import os
import json


"""
VARIÁVEIS:
1. arquivo_coord: nome do arquivo com as coordenadas dos bairros do Recife
2. pasta_dados_brutos: nome da pasta com os dados brutos do INMET
3. pasta_dados_ano: nome da pasta com os dados processados por mês, por ano
4. estacao: código da estação automática de Recife
5. anos: período de tempo para o qual se deseja organizar os dados
6. pasta_temperatura: destino final da temperatura por ano, por mês e por bairro
7. pasta_vento: destino final da velocidade dos ventos por ano, por mês e por bairro
8. pasta_umidade_relativa: destino final da umidade relativa do ar por ano, por mês e por bairro
9. coord: dataframe com as coordenadas dos bairros de Recife
"""

# Lê parâmetros do config.json
with open("config.json", "r") as f:
    config = json.load(f)
params = config["dados_INMET"]

# Parâmetros
arquivo_coord = params["arquivo_coord"]
pasta_dados_brutos = params["pasta_dados_brutos"]
pasta_dados_ano = params["pasta_dados_ano"]
estacao = params["estacao"]
anos = params["anos"]
pasta_temperatura = params["pasta_temperatura"]
pasta_vento = params["pasta_vento"]
pasta_umidade_relativa = params["pasta_umidade_relativa"]

# Organizando as coordenadas dos bairros
if arquivo_coord == "coordenadas-bairros-recife.csv":
    coord = pd.read_csv(os.path.join(os.getcwd(), "coordenadas-bairros-recife.csv"), delimiter=',')
    coord.sort_values(by='Bairro', inplace=True)
    coord.drop(["latitude-WGS84", "longitude-WGS84"], inplace=True, axis=1)
if arquivo_coord == "coordenadas-bairros-recife-criadouros.xlsx":
    coord = pd.read_excel(os.path.join(os.getcwd(), arquivo_coord))
    coord.drop(["Código", "latitude-WGS84", "longitude-WGS84"], inplace=True, axis=1)

# criando as pastas para salvar os dados do INMET processados por ano, por mês e por bairro
os.makedirs(pasta_temperatura, exist_ok=True)
os.makedirs(pasta_vento, exist_ok=True)
os.makedirs(pasta_umidade_relativa, exist_ok=True)

# descompactando os arquivos ".zip" apenas para a estação do Recife
for ano in anos:
    extract_zipped_files.extract(estacao, pasta_dados_brutos, ano)
        
# Selecionando os arquivos para processar
arquivos_dados_brutos = [
    os.path.join(pasta_dados_brutos, arquivo)
    for arquivo in os.listdir(pasta_dados_brutos)
]
arquivos_processamento = []

for ano in anos:
    for arquivo in arquivos_dados_brutos:
        if arquivo.split("-")[-1].split(".CSV")[0] == ano:
            arquivos_processamento.append(arquivo)

# processando os dados do INMET
for file in arquivos_processamento:
    filename = processINMETdata.fill_missing_values(file)  # lidando com os dados faltantes
    INMET_data_per_year = processINMETdata.dados_por_ano(filename)  # organizando os dados por ano

    # distribuição da temperatura por bairro
    processINMETdata.NeighbourhoodClimaticVariables(
        filename=INMET_data_per_year,
        coordinates=coord,
        variable="temp",
        folder=pasta_temperatura
    )

    # distribuição da velocidade dos ventos por bairro
    processINMETdata.NeighbourhoodClimaticVariables(
        filename=INMET_data_per_year,
        coordinates=coord,
        variable="vento",
        folder=pasta_vento
    )

    # distribuição da umidade relativa do ar por bairro
    processINMETdata.NeighbourhoodClimaticVariables(
        filename=INMET_data_per_year,
        coordinates=coord,
        variable="umidade",
        folder=pasta_umidade_relativa
    )
