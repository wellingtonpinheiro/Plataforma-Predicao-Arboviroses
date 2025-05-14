import processDadosAbertosData
import numpy as np
import pandas as pd
import os
import json


def get_last_year_bimester(year):
    # nome do arquivo do ano anterior
    filename = "arboviroses" + year + "_nov-dez"
    filename = os.path.join("quantidade de casos confirmados", "arboviroses " + year, filename)

    # abrindo o arquivo do último bimestre do ano anterior ao ano em questão
    if os.path.exists(filename):
        data = pd.read_csv(filename)
        number_of_cases = data['quantidade de casos confirmados'].values
        return number_of_cases


# Lê parâmetros do config.json
with open("config.json", "r") as f:
    config = json.load(f)
params = config["dados_casos"]

# Parâmetros
pasta_arquivos_dengue = params["pasta_dengue"]
pasta_arquivos_zika = params["pasta_zika"]
pasta_arquivos_chikungunya = params["pasta_chikungunya"]
pasta_arboviroses = params["pasta_casos"]
arquivo_coordenadas = params["arquivo_coord"]
anos = params["anos"]


# lendo as coordenadas dos bairros do Recife
coord = pd.read_csv(arquivo_coordenadas)
coord.sort_values(by=['Bairro'], inplace=True)
coord.drop(["Y", "X"], inplace=True, axis=1)

arboviroses_bimestres = []  # lista que armazena os valores dos casos por bimestre

# criando a pasta para guardar os arquivos com casos contabilizadoos
os.makedirs(pasta_arboviroses, exist_ok=True)
#######################################################

# listando os arquivos com os casos de cada uma das arboviroses
arquivos_dengue = os.listdir(pasta_arquivos_dengue)
arquivos_chikungunya = os.listdir(pasta_arquivos_chikungunya)
arquivos_zika = os.listdir(pasta_arquivos_zika)

for ano in anos:
    # identificando os bimestres
    bimestres = [(ano + "-01", ano + "-02"),
                 (ano + "-03", ano + "-04"),
                 (ano + "-05", ano + "-06"),
                 (ano + "-07", ano + "-08"),
                 (ano + "-09", ano + "-10"),
                 (ano + "-11", ano + "-12")]

    # lendo o arquivo para cada um dos casos
    arquivo_dengue = [os.path.join(pasta_arquivos_dengue, arquivo) for arquivo in arquivos_dengue if ano in arquivo][0]
    arquivo_chikungunya = [os.path.join(pasta_arquivos_chikungunya, arquivo) for arquivo in arquivos_chikungunya
                           if ano in arquivo]
    arquivo_zika = [os.path.join(pasta_arquivos_zika, arquivo) for arquivo in arquivos_zika if ano in arquivo]

    # contagem dos casos
    for i in range(0, len(bimestres)):
        casos_dengue = np.array(processDadosAbertosData.countCases(file=arquivo_dengue,
                                                                   bimester=bimestres[i],
                                                                   coordinates=coord))
        if len(arquivo_zika) != 0:
            casos_zika = np.array(processDadosAbertosData.countCases(file=arquivo_zika[0],
                                                                     bimester=bimestres[i],
                                                                     coordinates=coord))
        else:
            casos_zika = np.array(len(coord["Bairro"].values)*[0])

        if len(arquivo_chikungunya) != 0:
            casos_chikungunya = np.array(processDadosAbertosData.countCases(file=arquivo_chikungunya[0],
                                                                            bimester=bimestres[i],
                                                                            coordinates=coord))
        else:
            casos_chikungunya = np.array(len(coord["Bairro"].values)*[0])

        # calculando a quantidade total de casos de arboviroses para cada um dos bairros
        casos_totais = casos_dengue + casos_zika + casos_chikungunya
        arboviroses_bimestres.append(casos_totais)
        """
        quando o bimestre em questão não tem casos confirmados, então, a quantidade de casos é igual à quantidade de
        casos do bimestre anterior
        
        """
        if np.all(casos_totais == 0) and bimestres[i] != (ano + "01", ano + "02"):
            arboviroses_bimestres[i] = arboviroses_bimestres[i - 1]

        if np.all(casos_totais == 0) and bimestres[i] == (ano + "-01", ano + "-02") and ano != '2013':
            arboviroses_bimestres[i] = get_last_year_bimester(year=str(int(ano) - 1))

        # salvando o arquivo de casos por bimestres

        df_casos = pd.DataFrame({"bairro": coord['Bairro'].values,
                                 "latitude": coord['latitude-WGS84'].values,
                                 "longitude": coord['longitude-WGS84'].values,
                                 "quantidade de casos": arboviroses_bimestres[i]})

        processDadosAbertosData.save_csv(data=df_casos,
                                         bimester=bimestres[i],
                                         year=ano,
                                         file="casosArboviroses_",
                                         folder=pasta_arboviroses)

    arboviroses_bimestres = []
