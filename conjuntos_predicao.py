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
pasta_dados_bimestres = "quantidade casos"  # pasta que contém o conjunto de dados bimestrais
arquivo_coord = "coordenadas-bairros-recife.csv"  # arquivo com as coordenadas dos bairros
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
