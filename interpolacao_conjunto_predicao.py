"""
Código para montar os conjuntos de predição com os mapas interpolados.
Para cada bimestre, de cada ano, os dados são concatenados na seguinte ordem
(considere os seis bimestres que antecedem o bimestre de predição):

1. Bairro;
2. Latitude;
3. Longitude;
4. Casos (ou criadouros) por bimestre;
5. Temperatura (para os meses do bimestre);
6. Pluviometria (para os meses do bimestre);
7. Velocidade dos ventos (para os meses do bimestre);
8. Umidade relativa do ar (para os meses do bimestre).

* OBS 1: Para executar este código, é necessário ter o shapefile da cidade do Recife.
* OBS 2: O usuário deve ter instalado o R e os pacotes "raster", "terra", "sp", "sf" e "gstat".
* OBS 3: O usuário deve possuir o arquivo com as grades de interpolação (grid) para que o código funcione corretamente.

Criado por: Equipe de Geo-saúde do grupo de Computação Biomédica (DEBM-UFPE)  
Data: 30/04/2022  
Última atualização: 10/11/2023  
Contatos: cll@ecomp.poli.br, acgs@ecomp.poli.br, wellington.santos@ufpe.br
"""

import interpolacao
import os
import json

# Lê os parâmetros a partir do arquivo de configuração
with open("config.json", "r") as f:
    config = json.load(f)

# Tipo de análise: 'quantidade casos' ou 'infestacao predial'
tipo = config["tipo_analise"]

# Parâmetros de predição e interpolação para o tipo escolhido
params_predicao = config["dados_predicao"][tipo]
params_interp = config["interpolacao_predicao"]

# Diretórios de entrada e saída conforme o tipo de análise
if tipo == "casos":
    pasta_arquivos_conjuntos = params_interp["casos"]["pasta_conjuntos_predicao"]
    pasta_conjuntos_interpolados = params_interp["casos"]["pasta_conjuntos_interpolados"]
elif tipo == "criadouros":
    pasta_arquivos_conjuntos = params_interp["criadouros"]["pasta_conjuntos_predicao"]
    pasta_conjuntos_interpolados = params_interp["criadouros"]["pasta_conjuntos_interpolados"]
else:
    raise ValueError(f"Tipo de análise inválido no config.json: {tipo}")


caminho_R = params_interp["caminho_rscript"]

# Cria a pasta para salvar os arquivos interpolados, se não existir
os.makedirs(pasta_conjuntos_interpolados, exist_ok=True)

# Geração dos conjuntos interpolados via função principal da biblioteca 'interpolacao'
interpolacao.Interpolation(
    folder1=pasta_arquivos_conjuntos,
    folder2=os.path.join(os.getcwd(), pasta_conjuntos_interpolados),
    rscript_path=r"C:\Program Files\R\R-4.5.0\bin\Rscript.exe"
)
