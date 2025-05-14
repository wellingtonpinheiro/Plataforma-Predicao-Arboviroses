"""
Código para a organização dos dados das notificações de casos de dengue zika e chikungunya do Portal
de Dados Abertos da Prefeitura da cidade do Recife

Criado por: Equipe de Geo-saúde do grupo de Computação Biomédica (DEBM-UFPE)
Data: 30/04/2022
Última atualização: 10/11/2023
contatos: cll@ecomp.poli.br, acgs@ecomp.poli.br, wellington.santos@ufpe.br
"""


import pandas as pd
import processDadosAbertosData
import os

"""
VARIÁVEIS DO CÓDIGO

1. pasta_arquivos: pasta onde os arquivos baixados diretamente do Portal de Dados Abertos estão armazenados
2. arbovirose: tipo de arbovirose para as quais os dados serão organizados
3. anos: lista com os anos para os quais se deseja organizar os dados das arboviroses
4. arquivo_coordenadas: nome do arquivo com as coordenadas dos bairros do Recife
5. coord: dataframe com as coordenadas de cada bairro da cidade do Recife
6. arquivo_arbovirose: lista com os arquivos que estão na pasta_arquivos
7. nome_arquivo: nome do arquivo que está na lista arquivo_arbovirose para um ano em específico
8. casos: dataframe com os casos processados do arquivo nome_arquivo

"""

############### parâmetros iniciais ################
pasta_arquivos = "notificacoes dengue"
arbovirose = "dengue"
anos = ['2015']  # lista com os anos para os quais se deseja organizar os dados
arquivo_coordenadas = "coordenadas-bairros-recife.csv"

# organizando as coordenadas dos bairros do Recife
coord = pd.read_csv(arquivo_coordenadas, delimiter=',')
coord.sort_values(by='Bairro', inplace=True)
coord.drop(["latitude-WGS84", "longitude-WGS84"], inplace=True, axis=1)
####################################################################3


"""
Os arquivos baixados do Portal de Dados Abertos da Prefeitura do Recife precisa passar por algumas correções 
antes de inicializarmos a contagem dos casos confirmados das arboviroses para cada um dos bairros.
1. A primeira correção é referente aos anos das notificações. Em algumas notificações foram salvas com os anos 
incorretos. Portanto, no algoritmo, cada notificação é salva para o seu respectivo ano.
2. Correção dos bairros. Algumas células dos bairros estão nulas ou os bairros não estão tendo o mesmo padrão de
escrita. Isto dificulta o processo de contagem, por isso, deve ser corrigido antes desse ser iniciado.
"""

arquivo_arbovirose = []

# buscando os arquivos dos casos de arboviroses
for root, dirs, files in os.walk(pasta_arquivos):
    for file in files:
        if file.endswith(".csv"):
            arquivo_arbovirose.append(os.path.join(root, file))

# organizando os dados do Portal de Dados Abertos
for ano in anos:
    nome_arquivo = [arquivo for arquivo in arquivo_arbovirose if ano in arquivo][0]

    # corrigindo os anos de notificação
    #processDadosAbertosData.check_year(ano, nome_arquivo)

    # corrigindo ps bairros das notificações
    print("Organizando os bairros dos casos de {}".format(arbovirose))
    casos = processDadosAbertosData.check_neigbourhood(nome_arquivo, coord)
    casos.to_csv(nome_arquivo, index=False)
