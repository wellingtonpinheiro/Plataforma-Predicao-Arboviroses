import pandas as pd
import os


def check_year(actual_year, filename):
    """
    Essa função tem o objetivo de fazer algumas modificações nos arquivos das noticações de dengue por ano. É feita
    uma análise para poder verificar se a data de notificação é compatível com o ano que está sendo avaliado. Caso não
    seja, o bloco do dataframe é salvo no ano correto. Essa correção só é feita se o arquivo de destino final existir.
    :param actual_year: ano que está sendo realizada a avaliação
    :param filename: nome do arquivo de destino das notificações que estão no arquivo "errado"
    :return: não retorna nada
    """

    dataframe = pd.read_csv(filename, delimiter=',')

    if "notificacao_ano" in dataframe.columns:
        years = [str(i) for i in dataframe["notificacao_ano"].unique()]
        dataframe['notificacao_ano'] = dataframe['notificacao_ano'].astype(int)
        if len(years) == 1 and years[0] == actual_year:
            print("Só tem dados de {} no arquivo: {}".format(actual_year, filename))
        else:
            for i in years:
                if i != actual_year:
                    wrong_year_data = dataframe.loc[(dataframe.notificacao_ano == int(i))]
                    index = wrong_year_data.index
                    dataframe = dataframe.drop(index, axis=0)
                    file = filename.split("_")[0] + "_" + i + ".csv"
                    if os.path.isfile(file):
                        new_data = pd.read_csv(file, delimiter=",")
                        pd.concat([new_data, wrong_year_data]).to_csv(file, index=False)
            dataframe.to_csv(filename, index=False)


def check_neigbourhood(file, coordinates):
    """
    Esta função o objetivo de checar se o nome dos bairros dos arquivos do Portal de Dados Abertos estão iguais aos
    bairros do arquivo "coordendas-bairros-recife.csv". O algoritmo segue o seguinte fluxo:
    1. Avalia se na coluna "no_bairro_residencia" existe alguma célula 'nan'. Caso exista, a linha correspondente é eli-
    minada, pois, desta forma, não tem como saber de que bairro é aquele caso.
    2. Avalia se os bairros do dataframe são equivalentes aos bairros do arquivo "coordendas-bairros-recife.csv". Se não
    for, o algoritmo pede para que o usuário corriga a informação. A informação deve ser corrigida conforme as orientações
    apresentadas.
    3. A função salva o arquivo com o nome corrigido.

    :param file: nome do arquivo que está sendo ajustado.
    :param coordinates: dataframe com o nome e coordenadas dos bairros da Cidade do Recife.
    :return: dataframe com os bairros corrigidos.
    """
    # nome do arquivo com os bairros removidos
    os.makedirs("bairros removidos", exist_ok=True)
    filename = "bairros_removidos_" + os.path.basename(file).split(".csv")[0] + ".csv"

    data = pd.read_csv(file, delimiter=',')

    # eliminando os campos vazios para os bairros
    data = data.dropna(subset=['no_bairro_residencia'])
    neighbourhood_not_found = []

    # listas dos bairros que estão nos arquivos dos casos confirmados e no arquivo "coordendas-bairros-recife.csv"
    neighbourhoods = list(coordinates['Bairro'].values)
    neighbourhoods_data = data['no_bairro_residencia'].to_list()  # os bairros do arquivo original
    neighbourhoods_data = [str(neighbourhood).strip() for neighbourhood in neighbourhoods_data]

    test = set(neighbourhoods_data).issubset(neighbourhoods)
    if not test:  # checando se os bairros são iguais
        for i in range(0, len(neighbourhoods_data)):
            if neighbourhoods_data[i] not in neighbourhoods:
                print('Ajustando o bairro da linha {}...'.format(str(i)))
                answer = input(
                    'Você reconhece o bairro {} (responder apenas com s ou n)? '.format(neighbourhoods_data[i]))
                if answer == 's':
                    print("Para informar o nome correto do bairro, siga as recomendações abaixo: \n"
                          "1. NÃO dê espaço antes de escrever o nome do bairro\n"
                          "2. Escreva o nome do bairro em CAIXA ALTA e SEM ACENTUAÇÃO!!! \n"
                          "3. Seja consistente com os nomes no arquivo coordenadas-bairros-recife.csv\n")
                    correct_neighbourhood = input("Informe o nome correto do bairro: ").strip()
                    neighbourhoods_data[i] = correct_neighbourhood
                if answer == 'n':
                    neighbourhoods_data[i] = neighbourhoods_data[i]
                    neighbourhood_not_found.append(neighbourhoods_data[i])

        data['no_bairro_residencia'] = neighbourhoods_data

        # removendo os bairros que não foram encontrados
        data = data[~data['no_bairro_residencia'].isin(neighbourhood_not_found)]

        removed_neighbourhoods = pd.DataFrame({"bairros removidos": neighbourhood_not_found})
        if not data.empty:
            removed_neighbourhoods.to_csv(os.path.join("bairros removidos", filename), index=True)

        print('As linhas correspondentes aos bairros {} foram eliminadas do arquivo.'.format(neighbourhood_not_found,
                                                                                             file))
        return data
    else:
        print("Todos os bairros estão corretos")
        return data


def cases_per_bimester(data, bimester):
    data = data.loc[(data.mes == bimester[0]) | (data.mes == bimester[1])]
    return data


def countCases(file, coordinates, bimester):
    # separar os bairros da cidade
    neighbourhoods = coordinates['Bairro'].values

    # inicializar contador de casos
    cases_neighbourhood = len(neighbourhoods) * [0]

    data = pd.read_csv(file)

    cases_bimester = cases_per_bimester(data, bimester)

    # separar por bairros
    for neighbourhood in neighbourhoods:
        idx = coordinates[coordinates['Bairro'] == neighbourhood].index
        temp = cases_bimester.loc[(cases_bimester.no_bairro_residencia == neighbourhood)]
        number_of_cases = temp.groupby('no_bairro_residencia').size()
        if len(number_of_cases) != 0:
            cases_neighbourhood[idx[0]] = number_of_cases[0]

    return cases_neighbourhood


def save_csv(data, bimester, year, file, folder):
    """
    Função para salvar o "csv" com a quantidade de casos supeitos e casos confirmados em cada um dos bairros do Recife.
    :param data: dataframe para salvar como csv (pode ser de casos confirmados ou casos suspeitos)
    :param bimester: bimestre da quantidade de casos
    :param year: ano dos dados
    :param file: nome do csv final
    :param folder: pasta em que vai ficar armazenado o csv final
    :return: a função não retorna nada
    """
    data = data

    # salvando o bimestre de janeiro/fevereiro
    if bimester == (year + "-01", year + "-02"):
        filename = file + year + "_01.csv"
        filename = os.path.join(folder, filename)
        if not os.path.exists(filename):
            data.to_csv(filename, index=False)
        else:
            print("O arquivo {} já existe!".format(filename))

    # salvando o bimestre de março/abril
    if bimester == (year + "-03", year + "-04"):
        filename = file + year + "_02.csv"
        filename = os.path.join(folder, filename)
        if not os.path.exists(filename):
            data.to_csv(filename, index=False)
        else:
            print("O arquivo {} já existe!!!".format(filename))

    # salvando o bimestre de maio/junho
    if bimester == (year + "-05", year + "-06"):
        filename = file + year + "_03.csv"
        filename = os.path.join(folder, filename)
        if not os.path.exists(filename):
            data.to_csv(filename, index=False)
        else:
            print("O arquivo {} já existe!!!".format(filename))

    # salvando o bimestre de julho/agosto
    if bimester == (year + "-07", year + "-08"):
        filename = file + year + "_04.csv"
        filename = os.path.join(folder, filename)
        if not os.path.exists(filename):
            data.to_csv(filename, index=False)
        else:
            print("O arquivo {} já existe!!!".format(filename))

    # salvando o bimestre de setembro/outubro
    if bimester == (year + "-09", year + "-10"):
        filename = file + year + "_05.csv"
        filename = os.path.join(folder, filename)
        if not os.path.exists(filename):
            data.to_csv(filename, index=False)
        else:
            print("O arquivo {} já existe!!!".format(filename))

    # salvando o bimestre de novembro/dezembro
    if bimester == (year + "-11", year + "-12"):
        filename = file + year + "_06.csv"
        filename = os.path.join(folder, filename)
        if not os.path.exists(filename):
            data.to_csv(filename, index=False)
        else:
            print("O arquivo {} já existe!!!".format(filename))
