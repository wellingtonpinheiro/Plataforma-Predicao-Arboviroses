import pandas as pd
import csv
import os


def pegarDelimitador(nome_arquivo_csv):
    with open(nome_arquivo_csv, 'r') as arquivocsv:
        dialect = csv.Sniffer().sniff(arquivocsv.readline())
        return dialect.delimiter


def ajusteDados(arquivo, tipo_arbovirose):
    """
    Função para ajustar os delimitadores dos arquivos csv do Portal de Dados Abertos (mudar de ";" para ",")
    :param tipo_arbovirose: variável com o tipo de arbovirose para fazer os ajustes do dataframe
    :param arquivo: nome do arquivo csv que contém os dados das notificações do SINAN
    :return: dados ajustados
    """
    # capturando o delimitador do arquivo csv
    delimitador = str(pegarDelimitador(arquivo))

    # abrindo o arquivo com a base de dados
    dados = pd.read_csv(arquivo, delimiter=delimitador)

    if tipo_arbovirose == 'zika':
        if "ano_notificacao" in dados.columns:
            dados.rename(columns={'ano_notificacao': 'notificacao_ano'}, inplace=True)

    # ordenando os dados de acordo com os bairros
    dados.sort_values(by=['no_bairro_residencia'], inplace=True)

    # lista das colunas do dataframe final
    colunas_df = ["dt_notificacao", "notificacao_ano", "no_bairro_residencia", "tp_classificacao_final", "mes"]

    # deletando as colunas que não serão utilizadas
    colunas = list(set(dados.columns.to_list()) - set(colunas_df))
    dados.drop(columns=colunas, inplace=True)

    # criando uma coluna para os meses (será importante para a contagem dos bimestres)
    if 'mes' not in dados:
        dados['mes'] = pd.to_datetime(dados['dt_notificacao']).dt.to_period('M')

    # deletar as linhas que contém células vazias para a coluna 'no_bairro_residencia'
    dados.dropna(subset=['no_bairro_residencia'], inplace=True)
    return dados


def main():
    # parâmetros iniciais
    pasta_arquivos_brutos = "dados brutos dengue"
    pasta_arquivos_ajustados = "notificacoes dengue"
    tipo_arbovirose = "dengue"

    # criando a pasta para os dados de notificacoes
    os.makedirs(pasta_arquivos_ajustados, exist_ok=True)

    # ajustando os delimitadores dos dados do portal de dados abertos
    arquivos = []  # lista de arquivos com os dados para serem ajustados
    for root, dirs, files in os.walk(pasta_arquivos_brutos):
        for file in files:
            if file.endswith(".csv"):
                arquivos.append(os.path.join(root, file))

    # limpeza inicial dos arquivos do Portal de Dados Abertos
    for arquivo in arquivos:
        print("Ajustando o arquivo {}".format(arquivo))
        dados_casos = ajusteDados(arquivo, tipo_arbovirose)
        nome_arquivo = os.path.basename(arquivo)
        dados_casos.to_csv(os.path.join(pasta_arquivos_ajustados, nome_arquivo), index=False)


main()
