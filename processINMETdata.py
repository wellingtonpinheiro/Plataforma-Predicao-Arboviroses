from datetime import datetime
from dateutil.relativedelta import relativedelta
import statistics
import pandas as pd
import numpy as np
import sys
import os
import csv


def stringToFloat(string_list):
    """
    Modifica, de string para float, os valores das leituras da estação escolhida pelo usuário.
    :param string_list: lista de valores que serão modificados
    :return: retorna o vetor string_list com as variáveis do tipo float
    """
    # OBS: modificar o tratamento dos índices que estão vazios
    # tranforma os valores da planilha que estão como "string" para "float"
    variable = [i.replace(",", ".") for i in string_list]
    float_values = []
    for i in range(len(variable)):
        if not variable[i]:  # quando não há nenhum valor no index i da lista, o programa substitui por -9999
            variable[i] = "-9999"
        float_values.append(float(variable[i]))

    return float_values


def substituteUnkownValues(data):
    """
    Esta função tem o objetivo de substituir os valores nulos das medições pela moda da distribuição.
    :param data: dataframe (com as medicoes por hora) com os valores -9999.0, que correspondem aos valores nulos das
    medições. Quando a moda tiver mais de um valor, então, o valor faltante é preenchido com a média da moda.
    :return: retorna um dataframe com os valores faltantes preechidos com a moda da distribuição.

    """
    read_values = []

    # lista apenas com os dados lidos
    for i in range(0, len(data - 1)):
        if data[i] != -9999.0:
            read_values.append(data[i])
    read_values = np.array(read_values)

    # calculando a moda
    sample_mode = statistics.multimode(read_values)
    sample_mode = np.array(sample_mode)

    # substuindo os valores faltantes pela moda
    for i in range(len(data)):

        if data[i] == -9999.0:
            if len(sample_mode) >= 2:
                data[i] = np.mean(sample_mode)
            else:
                data[i] = sample_mode[0]

    print(sample_mode)
    return data


def fill_missing_values(file_path):
    """
    Esta função faz o pré-processamento dos dados do INMET que foram baixados a partir dos dados baixados por meio do
    web scraper "scraper_INMET.py".
    Ajustes feitos nas bases de dados:
    1. Organiza os arquivos .csv;
        *TEMPERATURA DO AR - BULBO SECO, HORARIA (ÂC) = Temperatura instantânia
        *TEMPERATURA MAXIMA NA HORA ANT. (AUT) (Ã‚C) = Temperatura Máxima
        *TEMPERATURA MINIMA NA HORA ANT. (AUT) (Ã‚C) = Temperatura Mínima
        *UMIDADE REL. MAX. NA HORA ANT. (AUT) (%) = Umidade Máxima
        *UMIDADE RELATIVA DO AR, HORARIA (%) = Umidade Instantânia
        *UMIDADE REL. MIN. NA HORA ANT. (AUT) (%) = Umidade Mínima
        *VENTO, RAJADA MAXIMA (m/s) = Velocidade Máxima
        *VENTO, VELOCIDADE HORARIA (m/s) = Velocidade Instantânea
    2. Muda o tipo das variáveis de string para float
    3. Quando não há nenhuma leitura por parte das estações, substitui-se o "" por -9999. Esta substituição foi feita
    baseando-se nos arquivos do próprio INMET.

    :param file_path: caminho do arquivo para fazer o pré-processamento
    :return: esta função não retorna nenhum valor
    """
    # criando o diretório para poder salvar os dados pré-processados
    directory = os.path.join(os.getcwd(), "dados INMET")
    os.makedirs(directory, exist_ok=True)

    # nome do arquivo final preprocessado
    year = file_path.split("-")[-1].split(".CSV")[0]
    filename = os.path.join(directory, "dadosINMETdiario_" + year + ".csv")
    """
        1. TEMPERATURA DO AR - BULBO SECO, HORARIA (ÂC) = Temperatura instantânia
        2. TEMPERATURA MAXIMA NA HORA ANT. (AUT) (Ã‚C) = Temperatura Máxima
        3. TEMPERATURA MINIMA NA HORA ANT. (AUT) (Ã‚C) = Temperatura Mínima
        4. UMIDADE REL. MAX. NA HORA ANT. (AUT) (%) = Umidade Máxima
        5. UMIDADE RELATIVA DO AR, HORARIA (%) = Umidade Instantânea
        6. UMIDADE REL. MIN. NA HORA ANT. (AUT) (%) = Umidade Mínima
        7. VENTO, RAJADA MAXIMA (m/s) = Velocidade Máxima
        8. VENTO, VELOCIDADE HORARIA (m/s) = Velocidade Instantânea
    """

    counter = 0  # contador para armazenar a linha do csv que está sendo lido

    # nome das colunas do dataframe original
    columns = ["DATA (YYYY-MM-DD)", "HORA (UTC)", "PRECIPITACAO TOTAL, HORARIO (mm)",
               "PRESSAO ATMOSFERICA AO NIVEL DA ESTACAO, HORARIA (mB)",
               "PRESSAO ATMOSFERICA MAX.NA HORA ANT. (AUT) (mB)",
               "PRESSAO ATMOSFERICA MIN. NA HORA ANT. (AUT) (mB)", "RADIACAO GLOBAL (KJ/m2)",
               "TempInstantanea", "TEMPERATURA DO PONTO DE ORVALHO (Celsius)",
               "TempMaxima", "TempMinima",
               "TEMPERATURA ORVALHO MAX. NA HORA ANT. (AUT) (Celsius)",
               "TEMPERATURA ORVALHO MIN. NA HORA ANT. (AUT) (Celsius)",
               "UmidadeRelativaMaxima", "UmidadeRelativaMinima",
               "UmidadeRelativaInstantanea", "VENTO, DIREÇAO HORARIA (gr) (grau (gr))",
               "VelocidadeVentoMaxima",
               "VelocidadeVentoInstantanea", ""]

    data = np.ones(shape=20)

    if os.path.exists(filename):  # checando se o arquivo já foi processado
        print("O arquivo {} já foi ajustado".format(file_path))
        return filename
    else:
        with open(file_path) as csv_file:
            print("processando os dados do arquivo: {}".format(file_path))
            csv_reader = csv.reader(csv_file, delimiter=';')
            for row in csv_reader:
                if counter == 8:
                    columns = columns
                if counter >= 9:  # a partir da nona linha de cada CSV do INMET começa os dados coletados pelas estações
                    data = np.vstack((data, np.array(row)))
                counter = counter + 1
        data = np.delete(data, 0, 0)

        data = pd.DataFrame(data, columns=columns)

        # eliminando as colunas que não vão ser utilizadas
        labels = ["PRECIPITACAO TOTAL, HORARIO (mm)", "PRESSAO ATMOSFERICA AO NIVEL DA ESTACAO, HORARIA (mB)",
                  "PRESSAO ATMOSFERICA MAX.NA HORA ANT. (AUT) (mB)", "PRESSAO ATMOSFERICA MIN. NA HORA ANT. (AUT) (mB)",
                  "RADIACAO GLOBAL (KJ/m2)", "VENTO, DIREÇAO HORARIA (gr) (grau (gr))",
                  "TEMPERATURA DO PONTO DE ORVALHO (Celsius)",
                  "TEMPERATURA ORVALHO MAX. NA HORA ANT. (AUT) (Celsius)",
                  "TEMPERATURA ORVALHO MIN. NA HORA ANT. (AUT) (Celsius)", ""]

        data = data.drop(columns=labels)

        try:

            # processando os dados de temperatura
            print("Processando os dados da temperatura...")

            # Transformando os valores de string para float
            data["TempMaxima"] = stringToFloat(data["TempMaxima"].values.tolist())
            data["TempMinima"] = stringToFloat(data["TempMinima"].values.tolist())
            data["TempInstantanea"] = stringToFloat(data["TempInstantanea"].values.tolist())

            # Substituindo os valores -9999.0 (valores desconhecidos) pela moda da distribuição
            data["TempInstantanea"] = substituteUnkownValues(data["TempInstantanea"].values)
            data['TempMaxima'] = substituteUnkownValues(data["TempMaxima"].values)
            data["TempMinima"] = substituteUnkownValues(data["TempMinima"].values)

            # processando os dados da velocidade dos ventos
            print("Processando os dados de velocidade dos ventos...")

            # Transformando os valores de string para float
            data["VelocidadeVentoMaxima"] = stringToFloat(data["VelocidadeVentoMaxima"].values.tolist())
            data["VelocidadeVentoInstantanea"] = stringToFloat(data["VelocidadeVentoInstantanea"].values.tolist())

            # Substituindo os valores -9999.0 (valores desconhecidos) pela moda da distribuição
            data["VelocidadeVentoMaxima"] = substituteUnkownValues(data["VelocidadeVentoMaxima"].values)
            data["VelocidadeVentoInstantanea"] = substituteUnkownValues(data["VelocidadeVentoInstantanea"].values)

            # processando dados da umidade relativa do ar
            print("Processar os dados da umidade relativa do ar...")

            # Transformando os valores de string para float
            data["UmidadeRelativaMaxima"] = stringToFloat(data["UmidadeRelativaMaxima"].values.tolist())
            data["UmidadeRelativaMinima"] = stringToFloat(data["UmidadeRelativaMinima"].values.tolist())
            data["UmidadeRelativaInstantanea"] = stringToFloat(data["UmidadeRelativaInstantanea"].values.tolist())

            # Substituindo os valores -9999.0 (valores desconhecidos) pela moda da distribuição
            data["UmidadeRelativaMinima"] = substituteUnkownValues(data["UmidadeRelativaMinima"].values)
            data["UmidadeRelativaMaxima"] = substituteUnkownValues(data["UmidadeRelativaMaxima"].values)
            data["UmidadeRelativaInstantanea"] = substituteUnkownValues(data["UmidadeRelativaInstantanea"].values)

            # salvando os dados do pre-processamento
            data.to_csv(filename, index=False)
            return filename

        except "Não foi possível converter os dados do arquivo {}".format(file_path) as error:
            print(error)
            sys.exit()


def TempCompensada(dados_por_hora, tempMax, tempMin):
    """
    Essa função tem o objetivo de calcular a temperatura compensada do dia. O cálculo da temperatura compensada é dada por:

                                        Tmc = (TM + Tm + T12 + (2*T24))/5

    em que:
    Tmc --> é a temperatura média compensada do ar
    TM --> é a temperatura máxima diária
    Tm --> é a temperatura  mínima diária
    T12 --> temperatura do ar às 12h
    T24 --> temperatura do ar às 24h
    :return: essa função retorna a temperatura média compensada do ar
    """

    tempComp = []
    dates = dados_por_hora["DATA (YYYY-MM-DD)"].unique()

    for i in range(0, len(dates)):
        T12 = dados_por_hora.loc[(dados_por_hora['DATA (YYYY-MM-DD)'] == dates[i])
                                 & (dados_por_hora["HORA (UTC)"] == "12:00")]["TempInstantanea"].values
        T24 = dados_por_hora.loc[(dados_por_hora['DATA (YYYY-MM-DD)'] == dates[i])
                                 & (dados_por_hora["HORA (UTC)"] == "00:00")]["TempInstantanea"].values
        daily_tempComp = (tempMax[i] + tempMin[i] + T12[0] + (2 * T24[0])) / 5
        tempComp.append(daily_tempComp)

    return np.round(np.array(tempComp), decimals=3)


def monthlyValues(df):
    """
    Esta função tem como objetivo calcular as médias mensais de temperatura (máxima e compensada), umidade relativa do
    ar (máxima e instantânea) e velocidade dos ventos (máxima e instantânea).
    :param df: dataframe com os valores diários das medições de temperatura, umidade relativa do ar e velocidade dos ventos
    :return: dataframe com as médias mensais das variáveis climáticas citadas acima.

    """

    # separando os meses do ano
    df['DATA (YYYY-MM-DD)'] = df["DATA (YYYY-MM-DD)"].astype('datetime64[ns]')
    df.sort_values(by='DATA (YYYY-MM-DD)', inplace=True)
    df['mes'] = df["DATA (YYYY-MM-DD)"].dt.month
    months = df['mes'].unique()

    """ 
        CÁLCULO DOS VALORES MENSAIS:

        monthly_mean_TempMax -> média mensal da temperatura máxima
        monthly_mean_TempComp -> média mensal da temperatura média compensada
        monthly_mean_MaxWindSpeed -> média mensal da velocidade dos ventos máxima
        monthly_mean_instWindSpeed -> média mensal velocidade dos ventos instantânea
        monthly_mean_MaxHumidity -> média mensal da umidade relativa do ar máxima
        monthly_mean_instHumidity -> média mensal da umidade relativa do ar instantânea
        
        * a média calculada é a média aritmética
    """

    # calculando as médias mensais da temperatura
    monthly_mean_TempMax = np.array([df.loc[(df["mes"] == month)]['TempMaxima'].values.mean() for month in months])

    monthly_mean_TempComp = np.array([df.loc[(df["mes"] == month)]['TempMediaCompensada'].values.mean()
                                      for month in months])

    # calculando as médias mensais da velocidade do vento
    monthly_mean_MaxWindSpeed = np.array([df.loc[(df["mes"] == month)]['VelocidadeMaxima'].values.mean()
                                          for month in months])

    monthly_mean_instWindSpeed = np.array([df.loc[(df["mes"] == month)]['VelocidadeInstantaneaMedia'].values.mean()
                                           for month in months])

    # calculando as médias mensais da umidade relativa do ar
    monthly_mean_MaxHumidity = np.array([df.loc[(df["mes"] == month)]['UmidadadeMaxima'].values.mean()
                                         for month in months])

    monthly_mean_instHumidity = np.array([df.loc[(df["mes"] == month)]['UmidadeInstantaneaMedia'].values.mean()
                                          for month in months])

    # Montando o dataframe com os valores mensais
    columns_monthly_df = ["Months", "TempMaximaMedia", "TempCompensadaMedia", "VelocidadeMaximaMedia",
                          "VelocidadeInstantaneaMedia", "UmidadadeMaximaMedia", "UmidadeInstantaneaMedia"]

    monthly_values = np.hstack((months.reshape(len(months), 1),
                                monthly_mean_TempMax.reshape(len(monthly_mean_TempMax), 1),
                                monthly_mean_TempComp.reshape(len(monthly_mean_TempComp), 1),
                                monthly_mean_MaxWindSpeed.reshape(len(monthly_mean_MaxWindSpeed), 1),
                                monthly_mean_instWindSpeed.reshape(len(monthly_mean_instWindSpeed), 1),
                                monthly_mean_MaxHumidity.reshape(len(monthly_mean_MaxHumidity), 1),
                                monthly_mean_instHumidity.reshape(len(monthly_mean_instHumidity), 1)))

    montlhy_df = pd.DataFrame(monthly_values, columns=columns_monthly_df)

    return montlhy_df


def correct_UTC_column(df_column):
    # ajusta a coluna relacionada aos horários das medições

    df_column = df_column.to_list()
    list_hour = []  # lista para armazenar os horários das medições das estações meteorológicas

    for i in range(len(df_column)):
        if ":" not in df_column[i]:
            temp = df_column[i].split(" ")[0]
            temp = temp[0] + temp[1] + ":" + temp[2] + temp[3]
            list_hour.append(temp)
        else:
            list_hour.append(df_column[i])
    return list_hour


def dailyValues(df):
    # ajustando a coluna "HORA (UTC)" para o tipo datetime
    try:
        df['HORA (UTC)'] = df['HORA (UTC)'].astype('datetime64')
    except:
        df['HORA (UTC)'] = correct_UTC_column(df['HORA (UTC)'])

    df.sort_values(by="DATA (YYYY-MM-DD)", inplace=True)
    dates = df["DATA (YYYY-MM-DD)"].unique()

    """ 
    CÁLCULO DOS VALORES DIÁRIOS:
    daily_maxHumidity -> valor máximo da umidade que foi medido no dia
    daily_mean_instHumidity -> média (aritmética) das medições de temperatura instantânea
    daily_maxWindSpeed -> valor máximo da velocidade do vento no dia
    daily_mean_instWindSpeed -> média (aritmética) das medições da velocidade dos ventos no dia
    daily_tempMax -> valor máximo da temperatura no dia
    daily_tempComp -> valor da temperatura média compensada     

    """

    # calculando a média diária da umidade relativa do ar
    daily_maxHumidity = np.array(
        [df.loc[(df["DATA (YYYY-MM-DD)"] == date)]['UmidadeRelativaMaxima'].values.max()
         for date in dates])

    daily_mean_instHumidity = np.array([
        df.loc[(df["DATA (YYYY-MM-DD)"] == date)]['UmidadeRelativaInstantanea'].values.mean()
        for date in dates])

    # calculando a média diária da velocidade dos ventos
    daily_maxWindSpeed = np.array(
        [df.loc[(df["DATA (YYYY-MM-DD)"] == date)]['VelocidadeVentoMaxima'].values.max() for date in dates])

    daily_mean_instWindSpeed = np.array(
        [df.loc[(df["DATA (YYYY-MM-DD)"] == date)]['VelocidadeVentoInstantanea'].values.mean() for date in dates])

    # Calculando as temperaturas (máxima e mínima) diárias
    daily_tempMax = np.array([df.loc[(df["DATA (YYYY-MM-DD)"] == date)]['TempMaxima'].values.max() for date in dates])

    daily_tempMin = np.array([df.loc[(df["DATA (YYYY-MM-DD)"] == date)]['TempMinima'].values.min() for date in dates])

    # Calculando a temperatura média compensada
    daily_tempComp = TempCompensada(df, daily_tempMax, daily_tempMin)

    # Montando o dataframe com os valores diários
    columns_daily_df = ["DATA (YYYY-MM-DD)", "TempMaxima", "TempMediaCompensada", "VelocidadeMaxima",
                        "VelocidadeInstantaneaMedia", "UmidadadeMaxima", "UmidadeInstantaneaMedia"]

    daily_values = np.hstack((dates.reshape(len(dates), 1),
                              daily_tempMax.reshape(len(daily_tempMax), 1),
                              daily_tempComp.reshape(len(daily_tempComp), 1),
                              daily_maxWindSpeed.reshape(len(daily_maxWindSpeed), 1),
                              daily_mean_instWindSpeed.reshape(len(daily_mean_instWindSpeed), 1),
                              daily_maxHumidity.reshape(len(daily_maxHumidity), 1),
                              daily_mean_instHumidity.reshape(len(daily_mean_instHumidity), 1)))

    daily_df = pd.DataFrame(daily_values, columns=columns_daily_df)
    # print(daily_df)

    return daily_df


def dados_por_ano(file):
    # criando uma pasta para salvar os arquivos das variáveis separados por ano

    directory = os.path.join(os.getcwd(), "dados INMET por ano")
    os.makedirs(directory, exist_ok=True)

    # nome final do arquivo
    year = file.split("_")[1].split(".csv")[0]
    filename = os.path.join(directory, "dadosINMET_" + year + ".csv")

    if os.path.exists(filename):
        print("O arquivo {} já foi ajustado".format(filename))
        return filename
    else:
        data = pd.read_csv(file)

        # Calculando os valores diários das variáveis climaticos
        daily_climatic_variables = dailyValues(data)

        # calculando os dados por mês
        monthly_climatic_variables = monthlyValues(daily_climatic_variables)

        # salvando o arquivo com os valores mensais
        monthly_climatic_variables.to_csv(filename, index=False)

        return filename


def standard_deviation(mean, max_value):
    return abs((max_value - mean) / 4)


def NeighbourhoodClimaticVariables(filename, coordinates, variable, folder):
    # ano do arquivo
    year = os.path.basename(filename).split("_")[1].split(".csv")[0]

    # inicialização de alguma variáveis
    col_maxValue = 0
    col_meanValue = 0

    # colocar os critérios de nomeação do arquivo

    if variable == 'temp':
        col_maxValue = "TempMaximaMedia"
        col_meanValue = "TempCompensadaMedia"

    if variable == 'vento':
        col_maxValue = 'VelocidadeMaximaMedia'
        col_meanValue = 'VelocidadeInstantaneaMedia'

    if variable == 'umidade':
        col_maxValue = 'UmidadadeMaximaMedia'
        col_meanValue = 'UmidadeInstantaneaMedia'

    # criando o nome do arquivo do destino final
    final_filename = os.path.join(os.getcwd(), folder, "distribuicao_" + variable + year + ".csv")

    data = pd.read_csv(filename)  # ler os arquivos com as distribuições mensais
    data.sort_values(by='Months', inplace=True)
    months = data['Months'].values

    data.drop(["Months"], inplace=True, axis=1)

    finalData_columns = ['bairro', 'latitude', 'longitude', 'jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago',
                         'set', 'out', 'nov', 'dez']

    if os.path.exists(final_filename):
        print("O arquivo {} já foi criado".format(final_filename))
    else:
        for i in range(len(months)):
            # calculando o desvio padrao da distribuição
            maxValue = float(data[col_maxValue][i])  # valor máximo da distribuicao
            meanValue = float(data[col_meanValue][i])  # valor da média da distribuição
            std = standard_deviation(mean=meanValue, max_value=maxValue)

            # distribution for the neighbourhoods
            neigbourhood_distribution = abs(np.random.normal(meanValue, std, size=len(coordinates)))
            coordinates = np.hstack((coordinates, neigbourhood_distribution.reshape(len(neigbourhood_distribution), 1)))

        final_dataset = pd.DataFrame(coordinates, columns=finalData_columns)
        final_dataset.to_csv(final_filename, index=False)

# file = fill_missing_values(
#   r"C:\Users\clari\PycharmProjects\webCrawler\dados brutos INMET\INMET_NE_PE_A301_RECIFE_01-01-2021_A_31-12-2021.CSV")

# data_per_month = dados_por_ano(file=file)
# NeighbourhoodClimaticVariables(data_per_month)
