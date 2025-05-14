"""
Código para montar os conjuntos de predição com os mapas interpolados.
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

* OBS 1: para excutar esse código, é necessário ter o shapefile da cidade do Recife.
* OBS 2: o usuário deve ter instalado o R e os pacotes "raster", "terra", "sp", "sf" e "gstat"
* OBS 3: o usuário deve ter o arquivo com as grades de interpolação para que o código seja executado

Criado por: Equipe de Geo-saúde do grupo de Computação Biomédica (DEBM-UFPE)
Data: 30/04/2022
Última atualização: 10/11/2023
contatos: cll@ecomp.poli.br, acgs@ecomp.poli.br, wellington.santos@ufpe.br
"""

import interpolacao
import os
import json

# Lê parâmetros do config.json
with open("config.json", "r") as f:
    config = json.load(f)
params = config["interpolacao_predicao"]

# parâmetros iniciais
pasta_arquivos_conjuntos = params["pasta_conjuntos_predicao"]
pasta_conjuntos_interpolados = params["pasta_conjuntos_interpolados"]
caminho_R = params["caminho_rscript"]

# criando a pasta para salvar os arquivos interpolados
os.makedirs(pasta_conjuntos_interpolados, exist_ok=True)

# criando os conjuntos de interpolação
interpolacao.Interpolation(folder1=pasta_arquivos_conjuntos,
                           folder2="/" + pasta_conjuntos_interpolados,
                           path=caminho_R)

