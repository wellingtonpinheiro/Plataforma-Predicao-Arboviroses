"""
Programa para criar uma base de dados com as informações bimestrais de quantidade de casos confirmados de arboviroses, temperatura,
chuva e velocidade dos ventos para um determinado ano. Para o código ser executado, é importante que as pastas dos casos
de arboviroses, temperatura, chuva e velocidade dos ventos, estejam nomeadas como:

1. quantidade de casos confirmados (as subpastas devem ser nomeadas como "arboviroses + ano ". Ex: arboviroses 2013)
2. temperatura
3. distribuicao de chuva
4. vento

Além disso, o nome dos arquivos de cada uma das variáveis do problema devem estar na seguinte forma:

1. quantidade de casos confirmados: arboviroses + ano + _bimestre + extensão do arquivo. Ex: arboviroses2013_jan-fev.csv
2. temperatura: distribuicao_temp + ano + extensão do arquivo. Ex: distribuicao_temp2009.csv
3. distribuicao de chuva: distribuicao_chuva + ano + extensão do arquivo. Ex: distribuicao_chuva2009.csv
4. vento: distribuicao_vento + ano + extensão do arquivo. Ex: distribuicao_chuva2009.csv

Criado por: Equipe de Geo-saúde do grupo de Computação Biomédica (DEBM-UFPE)
Data: 30/04/2022
Última atualização: 10/11/2023
"""

# importando as bibliotecas necessárias

from itertools import chain
import pandas as pd
import numpy as np
import os
import subprocess


def filenames(folder):
    # Função para retornar a lista de arquivos de uma determinada pasta
    files_list = os.listdir(folder)
    files = [os.path.join(folder, filename) for filename in files_list]
    return files


def climaticVariable_bimesters(climatic_variables, folder, climaticVariableName):
    rainfall_bimesters_dataset = []

    # get the year and the bimester
    for i in range(len(climatic_variables)):
        aux = os.path.basename(climatic_variables[i]).split("_")
        year = aux[1]
        bimester = aux[2].split(".csv")[0]
        filename = os.path.join(folder, climaticVariableName + year + ".csv")

        # abrindo o arquivo do ano correspontente
        data = pd.read_csv(filename)

        if bimester == '01':
            rainfall_bimesters_dataset.append(data['jan'].values)
            rainfall_bimesters_dataset.append(data['fev'].values)
        if bimester == '02':
            rainfall_bimesters_dataset.append(data['mar'].values)
            rainfall_bimesters_dataset.append(data['abr'].values)
        if bimester == '03':
            rainfall_bimesters_dataset.append(data['mai'].values)
            rainfall_bimesters_dataset.append(data['jun'].values)
        if bimester == '04':
            rainfall_bimesters_dataset.append(data['jul'].values)
            rainfall_bimesters_dataset.append(data['ago'].values)
        if bimester == '05':
            rainfall_bimesters_dataset.append(data['set'].values)
            rainfall_bimesters_dataset.append(data['out'].values)
        if bimester == '06':
            rainfall_bimesters_dataset.append(data['nov'].values)
            rainfall_bimesters_dataset.append(data['dez'].values)

    print(len(rainfall_bimesters_dataset))
    return rainfall_bimesters_dataset


def save_csv(bimester, data, filename):
    # lista com o nome das colunas
    columns = []

    if bimester == '01':
        columns = ["Bairro", "latitude", "longitude",
                   "cb1", "t1b1", "t2b1", "p1b1", "p2b1", "v1b1", "v2b1", "ur1b1", "ur2b1",
                   "cb2", "t1b2", "t2b2", "p1b2", "p2b2", "v1b2", "v2b2", "ur1b2", "ur2b2",
                   "cb3", "t1b3", "t2b3", "p1b3", "p2b3", "v1b3", "v2b3", "ur1b3", "ur2b3",
                   "cb4", "t1b4", "t2b4", "p1b4", "p2b4", "v1b4", "v2b4", "ur1b4", "ur2b4",
                   "cb5", "t1b5", "t2b5", "p1b5", "p2b5", "v1b5", "v2b5", "ur1b5", "ur2b5",
                   "cb6", "t1b6", "t2b6", "p1b6", "p2b6", "v1b6", "v2b6", "ur1b6", "ur2b6","predicao"]

    if bimester == '02':
        columns = ["Bairro", "latitude", "longitude",
                   "cb2", "t1b2", "t2b2", "p1b2", "p2b2", "v1b2", "v2b2", "ur1b2", "ur2b2",
                   "cb3", "t1b3", "t2b3", "p1b3", "p2b3", "v1b3", "v2b3", "ur1b3", "ur2b3",
                   "cb4", "t1b4", "t2b4", "p1b4", "p2b4", "v1b4", "v2b4", "ur1b4", "ur2b4",
                   "cb5", "t1b5", "t2b5", "p1b5", "p2b5", "v1b5", "v2b5", "ur1b5", "ur2b5",
                   "cb6", "t1b6", "t2b6", "p1b6", "p2b6", "v1b6", "v2b6", "ur1b6", "ur2b6",
                   "cb1", "t1b1", "t2b1", "p1b1", "p2b1", "v1b1", "v2b1", "ur1b1", "ur2b1", "predicao"]

    if bimester == '03':
        columns = ["Bairro", "latitude", "longitude",
                   "cb3", "t1b3", "t2b3", "p1b3", "p2b3", "v1b3", "v2b3", "ur1b3", "ur2b3",
                   "cb4", "t1b4", "t2b4", "p1b4", "p2b4", "v1b4", "v2b4", "ur1b4", "ur2b4",
                   "cb5", "t1b5", "t2b5", "p1b5", "p2b5", "v1b5", "v2b5", "ur1b5", "ur2b5",
                   "cb6", "t1b6", "t2b6", "p1b6", "p2b6", "v1b6", "v2b6", "ur1b6", "ur2b6",
                   "cb1", "t1b1", "t2b1", "p1b1", "p2b1", "v1b1", "v2b1", "ur1b1", "ur2b1",
                   "cb2", "t1b2", "t2b2", "p1b2", "p2b2", "v1b2", "v2b2", "ur1b2", "ur2b2", "predicao"]

    if bimester == '04':
        columns = ["Bairro", "latitude", "longitude",
                   "cb4", "t1b4", "t2b4", "p1b4", "p2b4", "v1b4", "v2b4", "ur1b4", "ur2b4",
                   "cb5", "t1b5", "t2b5", "p1b5", "p2b5", "v1b5", "v2b5", "ur1b5", "ur2b5",
                   "cb6", "t1b6", "t2b6", "p1b6", "p2b6", "v1b6", "v2b6", "ur1b6", "ur2b6",
                   "cb1", "t1b1", "t2b1", "p1b1", "p2b1", "v1b1", "v2b1", "ur1b1", "ur2b1",
                   "cb2", "t1b2", "t2b2", "p1b2", "p2b2", "v1b2", "v2b2", "ur1b2", "ur2b2",
                   "cb3", "t1b3", "t2b3", "p1b3", "p2b3", "v1b3", "v2b3", "ur1b3", "ur2b3", "predicao"]

    if bimester == '05':
        columns = ["Bairro", "latitude", "longitude",
                   "cb5", "t1b5", "t2b5", "p1b5", "p2b5", "v1b5", "v2b5", "ur1b5", "ur2b5",
                   "cb6", "t1b6", "t2b6", "p1b6", "p2b6", "v1b6", "v2b6", "ur1b6", "ur2b6",
                   "cb1", "t1b1", "t2b1", "p1b1", "p2b1", "v1b1", "v2b1", "ur1b1", "ur2b1",
                   "cb2", "t1b2", "t2b2", "p1b2", "p2b2", "v1b2", "v2b2", "ur1b2", "ur2b2",
                   "cb3", "t1b3", "t2b3", "p1b3", "p2b3", "v1b3", "v2b3", "ur1b3", "ur2b3",
                   "cb4", "t1b4", "t2b4", "p1b4", "p2b4", "v1b4", "v2b4", "ur1b4", "ur2b4", "predicao"]

    if bimester == '06':
        columns = ["Bairro", "latitude", "longitude",
                   "cb6", "t1b6", "t2b6", "p1b6", "p2b6", "v1b6", "v2b6", "ur1b6", "ur2b6",
                   "cb1", "t1b1", "t2b1", "p1b1", "p2b1", "v1b1", "v2b1", "ur1b1", "ur2b1",
                   "cb2", "t1b2", "t2b2", "p1b2", "p2b2", "v1b2", "v2b2", "ur1b2", "ur2b2",
                   "cb3", "t1b3", "t2b3", "p1b3", "p2b3", "v1b3", "v2b3", "ur1b3", "ur2b3",
                   "cb4", "t1b4", "t2b4", "p1b4", "p2b4", "v1b4", "v2b4", "ur1b4", "ur2b4",
                   "cb5", "t1b5", "t2b5", "p1b5", "p2b5", "v1b5", "v2b5", "ur1b5", "ur2b5", "predicao"]

    # salvando o dataframe
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(filename, index=False)


def prediction_dataset(folder, coordinates, output_folder):
    """
    :param coordinates: coordenadas dos criadouros do mosquito aedes aegypti
    :param folder: a pasta da variável de predição. Ex: quantidade de casos confirmados ou criadouros
    :return: não retorna nenhum valor
    """

    # listando todos os arquivos/pastas presentes no diretório do projeto
    filename = " "
    df_column = " "
    rainfall_folder = " "
    wind_speed_folder = " "
    temp_folder = " "
    humidity_folder = " "
    folders = [os.path.join(os.getcwd(), file) for file in os.listdir(os.getcwd())]

    # listando os arquivos de casos
    files = list(chain(*[filenames(path) for path in folders if os.path.basename(path) == folder]))
    files.sort()

    for index in range(6, len(files)):
        # checando a existência do conjunto de predição
        print(files[index])
        aux = files[index]
        print(aux)
        year = os.path.basename(files[index]).split("_")[1]
        number_bimester = os.path.basename(files[index]).split("_")[2].split(".csv")[0]

        if folder == 'quantidade casos':
            filename = os.path.join(os.getcwd(), "dados predicao bimestres casos",
                                    "ConjuntoPredicaoArboviroses_" + str(year) + "_" + number_bimester + ".csv")
            df_column = 'quantidade de casos'
            rainfall_folder = 'distribuicao chuva'
            wind_speed_folder = "vento"
            temp_folder = "temperatura"
            humidity_folder = "umidade"

        if folder == 'infestacao predial':
            filename = os.path.join(os.getcwd(), "dados predicao bimestres criadouros",
                                    "criadouros_" + str(year) + "_" + number_bimester + ".csv")
            df_column = "total"
            rainfall_folder = "distribuicao chuva criadouros"
            wind_speed_folder = "vento criadouros"
            temp_folder = "temperatura criadouros"
            humidity_folder = "umidade relativa criadouros"

        if not os.path.exists(filename):
            # coletando os dados por bimestre
            bimester1 = pd.read_csv(files[index - 6], delimiter=',')
            bimester2 = pd.read_csv(files[index - 5], delimiter=',')
            bimester3 = pd.read_csv(files[index - 4], delimiter=',')
            bimester4 = pd.read_csv(files[index - 3], delimiter=',')
            bimester5 = pd.read_csv(files[index - 2], delimiter=',')
            bimester6 = pd.read_csv(files[index - 1], delimiter=',')
            pred_cases = pd.read_csv(files[index])  # dados do bimestre de predição

            # coletando as informações das variáveis climáticas
            bimesters = [files[index - 6],
                         files[index - 5],
                         files[index - 4],
                         files[index - 3],
                         files[index - 2],
                         files[index - 1]]

            rainfall = climaticVariable_bimesters(bimesters, rainfall_folder, "distribuicao_chuva")
            wind_speed = climaticVariable_bimesters(bimesters, wind_speed_folder, "distribuicao_vento")
            temperature = climaticVariable_bimesters(bimesters, temp_folder, "distribuicao_temp")
            humidity = climaticVariable_bimesters(bimesters, humidity_folder, "distribuicao_umidade")

            data = np.hstack((coordinates,
                              bimester1[df_column].values.reshape(len(bimester1[df_column]), 1),
                              temperature[0].reshape(len(temperature[0]), 1),
                              temperature[1].reshape(len(temperature[1]), 1),
                              rainfall[0].reshape(len(temperature[1]), 1),
                              rainfall[1].reshape(len(temperature[1]), 1),
                              wind_speed[0].reshape(len(wind_speed[0]), 1),
                              wind_speed[1].reshape(len(wind_speed[1]), 1),
                              humidity[0].reshape(len(humidity[0]), 1),
                              humidity[1].reshape(len(humidity[1]), 1),
                              bimester2[df_column].values.reshape(len(bimester2[df_column]), 1),
                              temperature[2].reshape(len(temperature[2]), 1),
                              temperature[3].reshape(len(temperature[3]), 1),
                              rainfall[2].reshape(len(temperature[2]), 1),
                              rainfall[3].reshape(len(temperature[2]), 1),
                              wind_speed[2].reshape(len(wind_speed[2]), 1),
                              wind_speed[3].reshape(len(wind_speed[3]), 1),
                              humidity[2].reshape(len(humidity[2]), 1),
                              humidity[3].reshape(len(humidity[3]), 1),
                              bimester3[df_column].values.reshape(len(bimester3[df_column]), 1),
                              temperature[4].reshape(len(temperature[4]), 1),
                              temperature[5].reshape(len(temperature[5]), 1),
                              rainfall[4].reshape(len(temperature[4]), 1),
                              rainfall[5].reshape(len(temperature[5]), 1),
                              wind_speed[4].reshape(len(wind_speed[4]), 1),
                              wind_speed[5].reshape(len(wind_speed[5]), 1),
                              humidity[4].reshape(len(humidity[4]), 1),
                              humidity[5].reshape(len(humidity[5]), 1),
                              bimester4[df_column].values.reshape(len(bimester4[df_column]), 1),
                              temperature[6].reshape(len(temperature[6]), 1),
                              temperature[7].reshape(len(temperature[7]), 1),
                              rainfall[6].reshape(len(temperature[6]), 1),
                              rainfall[7].reshape(len(temperature[7]), 1),
                              wind_speed[6].reshape(len(wind_speed[6]), 1),
                              wind_speed[7].reshape(len(wind_speed[7]), 1),
                              humidity[6].reshape(len(humidity[6]), 1),
                              humidity[7].reshape(len(humidity[7]), 1),
                              bimester5[df_column].values.reshape(len(bimester5[df_column]), 1),
                              temperature[8].reshape(len(temperature[8]), 1),
                              temperature[9].reshape(len(temperature[9]), 1),
                              rainfall[8].reshape(len(temperature[8]), 1),
                              rainfall[9].reshape(len(temperature[9]), 1),
                              wind_speed[8].reshape(len(wind_speed[8]), 1),
                              wind_speed[9].reshape(len(wind_speed[9]), 1),
                              humidity[8].reshape(len(humidity[8]), 1),
                              humidity[9].reshape(len(humidity[9]), 1),
                              bimester6[df_column].values.reshape(len(bimester6[df_column]), 1),
                              temperature[10].reshape(len(temperature[10]), 1),
                              temperature[11].reshape(len(temperature[11]), 1),
                              rainfall[10].reshape(len(temperature[10]), 1),
                              rainfall[10].reshape(len(temperature[11]), 1),
                              wind_speed[10].reshape(len(wind_speed[10]), 1),
                              wind_speed[11].reshape(len(wind_speed[10]), 1),
                              humidity[10].reshape(len(humidity[10]), 1),
                              humidity[11].reshape(len(humidity[11]), 1),
                              pred_cases[df_column].values.reshape(len(pred_cases[df_column]), 1)
                              ))
            save_csv(bimester=number_bimester, data=data, filename=filename)


def Interpolation(folder1, folder2, path):
    """
    :param folder2: pasta para salvar os mapas interpolados
    :param folder1: pasta com os arquivos ".csv" para interpolação
    :return:
    """
    # definir os comandos e argumentos que serão passados para o prompt de comando
    command = path
    path2script = os.path.join(os.getcwd(), 'interpolation.R')

    # build process command
    cmd = [command, '--vanilla', path2script, folder1, folder2]

    # check_output will run to the command and store result
    subprocess.call(cmd, shell=True)
    
    """
Código para montar os conjuntos de predição antes de enviar para a etapa de interpolação.
Para cada bimestre, de cada ano, os dados são concatenados, na seguinte ordem (considerando seis bimestres que antecedem
o bimestre de predição):
1. Bairro;
2. Latitude;
3. Longitude;
4. Casos (ou criadouros) por bimestre;
5. Temperatura (para os meses do bimestre);
6. Pluviometria (para os meses do bimestre);
7. Velocidade dos ventos (para os meses do bimestre);
8. Umidade relativa do ar (para os meses do bimestre)

Criado por: Equipe de Geo-saúde do grupo de Computação Biomédica (DEBM-UFPE)
Data: 30/04/2022
Última atualização: 10/11/2023
contatos: cll@ecomp.poli.br, acgs@ecomp.poli.br, wellington.santos@ufpe.br
"""

import pandas as pd
import dataset
import os

############ parâmetros iniciais ############
pasta_dados_bimestres = r"DADOS POR BAIRRO\CSV CRIADOUROS"  # pasta que contém o conjunto de dados bimestrais
arquivo_coord = r"DADOS POR BAIRRO\CSV CASOS"  # arquivo com as coordenadas dos bairros
pasta_conjuntos_bimestres = "dados predicao bimestres casos"
coord = 0  # inicialização da variável das coordenadas
#############################################

# criar pasta para salvar os cojuntos de predição por bimestre
os.makedirs(pasta_conjuntos_bimestres, exist_ok=True)

# Organizando as coordenadas dos bairros
if arquivo_coord == "coordenadas-bairros-recife.csv":
    coord = pd.read_csv(os.path.join(os.getcwd(), "coordenadas-bairros-recife.csv"), delimiter=',')
    coord.sort_values(by='Bairro', inplace=True)
    coord.drop(["X", "Y"], inplace=True, axis=1)
if arquivo_coord == "coordenadas-bairros-recife-criadouros.xlsx":
    coord = pd.read_excel(os.path.join(os.getcwd(), arquivo_coord))
    coord.drop(["Código", "X", "Y"], inplace=True, axis=1)

# Montando o conjunto de predicao
dataset.prediction_dataset(folder=pasta_dados_bimestres, coordinates=coord)
