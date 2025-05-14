import processAPACdata
import pandas as pd
import os
import json

# Lê parâmetros do config.json
with open("config.json", "r") as f:
    config = json.load(f)
params = config["dados_APAC"]

# Parâmetros
arquivo_coord = params["arquivo_coord"]
pasta_precipitacao = params["pasta_precipitacao"]
arquivo_dados_APAC = params["arquivo_dados_APAC"]
anos = params["anos"]

# Criando uma pasta para salvar os arquivos da APAC
os.makedirs("dados APAC", exist_ok=True)

# Organizando as coordenadas dos bairros
if arquivo_coord == "coordenadas-bairros-recife.csv":
    coord = pd.read_csv(os.path.join(os.getcwd(), arquivo_coord), delimiter=',')
    coord.sort_values(by='Bairro', inplace=True)
    coord.drop(["latitude-WGS84", "longitude-WGS84"], inplace=True, axis=1)
elif arquivo_coord == "coordenadas-bairros-recife-criadouros.xlsx":
    coord = pd.read_excel(os.path.join(os.getcwd(), arquivo_coord))
    coord.drop(["Código", "latitude-WGS84", "longitude-WGS84"], inplace=True, axis=1)

# Pré-processamento dos dados da APAC
processAPACdata.APAC_data(arquivo_dados_APAC)

# Processamento por ano
arquivos_processamento = [
    os.path.join(os.getcwd(), "dados APAC", filename)
    for filename in os.listdir(os.path.join(os.getcwd(), 'dados APAC'))
]

for ano in anos:
    arquivo_processamento = [arquivo for arquivo in arquivos_processamento if ano in arquivo][0]
    processAPACdata.rainfall_dataset(arquivo_processamento, coord, pasta_precipitacao)
