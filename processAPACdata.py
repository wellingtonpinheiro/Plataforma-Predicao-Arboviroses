import pandas as pd
import numpy as np
import os


def APAC_data(path):
    """

    Programa organizar os dados climáticos da APAC. Este programa executa as seguintes tarefas:

    1. Trata dos dados da APAC substituindo o separador decimal de "," para "." e substituindo
    os valores das estações sem registro de "-" para "0" por meio da função "APAC_data()."

    3. Separa por ano as informações sobre a precipitação mensal em cada uma das estações selecionadas no banco de dados
    da APAC (http://old.apac.pe.gov.br/meteorologia/monitoramento-pluvio.php#).

    Criado por: Equipe de Geo-saúde do grupo de pesquisa em Computação Biomédica DEBM-UFPE
    Data: 30/04/2022
    Última atualização: 15/08/2023


    :param path: caminho do arquivo .txt com os valores dos acumulados de chuva mensais obtidos do banco de dados da APAC
    :return: não retorna nenhum valor
    """

    # abrindo o arquivo da APAC
    data = pd.read_table(path)

    # mundando o separador decimal de ',' para '.'
    columns = data.iloc[:, 3:15].columns.values.tolist()
    data[columns] = data[columns].replace(',', '.', regex=True)

    # removendo os '-' para '0'
    data[columns] = data[columns].replace('-', '0', regex=True)
    data[columns] = data[columns].apply(pd.to_numeric)

    # capturando os anos para gerar arquivos por ano
    years = data['Ano'].values.tolist()

    # capturando os anos repetidos
    year = list(set(years))
    year.sort()

    # salvando os dados das variáveis climáticas por ano
    for i in range(len(year)):
        filtered_data = data.loc[data['Ano'] == year[i]]
        filename = "dadosAPAC_" + str(year[i]) + ".csv"
        filtered_data.to_csv(os.path.join(os.getcwd(), "dados APAC", filename), index=False)


def find_year(filename):
    # função para encontrar o ano da base de dados a partir do nome do arquivo
    aux = os.path.basename(filename).split("_")
    year = aux[1].split(".csv")
    return year[0]


def standard_deviation(mean, max_value):
    return (max_value - mean) / 4


def rainfall_dataset(file, dataset, final_folder):
    """
    Programa organizar os dados climáticos obtidos na base de dados da APAC. Este programa separa por ano as informações
    da distribuição das chuvas em cada um dos bairros da cidade do Recife.

    Para estimar a distribuição de chuvas em cada ponto da cidade, uma distribuição gauissiana foi
    utilizada, em que std = (x(max) - média)/4. No caso da APAC, os valores máximo e a média da amostra são os
    valores máximos e a média das estações que realizaram a coleta.


    :param final_folder: pasta do destino final
    :param file: nome do arquivo com os dados obtidos pelas estações da APAC
    :param dataset: conjunto de dados com o nome e coordenadas de cada bairro do Recife.
    :return: não retorna nenhum valor

    Criado por: Equipe de Geo-saúde do grupo de pesquisa em Computação Biomédica DEBM-UFPE
    Data: 30/04/2022
    Última atualização: 15/08/2023

    """

    size = len(dataset)
    dataframe_columns = ['bairro', 'latitude', 'longitude', 'jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago',
                         'set', 'out', 'nov', 'dez']

    # criando o diretório para poder salvar os dados pré-processados
    directory = os.path.join(os.getcwd(), final_folder)
    os.makedirs(directory, exist_ok=True)

    # nome do arquivo final preprocessado
    year = find_year(file)
    filename = os.path.join(directory, "distribuicao_chuva" + year + ".csv")

    if os.path.exists(filename):  # checando se o arquivo já foi processado
        print("O arquivo {} já foi ajustado".format(file))
    else:
        # for i in range(len(files)):
        data = pd.read_csv(file, delimiter=',')
        data.drop(["Código", "Posto", "Ano"], inplace=True, axis=1)
        columns = data.columns.values.tolist()
        for column in columns:
            mean_rainfall = data[column].mean()  # calculando média entre as medidas das estações
            max_rainfall = data[column].max()  # calculando o valor máximo dentre os valores medidos pelas estações
            std = standard_deviation(mean_rainfall, max_rainfall)  # cálculo do desvio padrão
            # estimando o valor da distribuição das chuvas em cada bairro da cidade
            month_rainfall = abs(np.random.normal(mean_rainfall, std, size=size))
            dataset = np.hstack((dataset, month_rainfall.reshape(len(month_rainfall), 1)))

        # criando um dataframe
        rainfall_dataframe = pd.DataFrame(dataset, columns=dataframe_columns)

        # salvando em um arquivo ".csv"
        rainfall_dataframe.to_csv(filename, index=False)
