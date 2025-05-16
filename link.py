import json
import subprocess
import os

# Carrega o config.json
with open("config.json", "r") as f:
    config = json.load(f)

tipo = config["tipo_analise"]  # "casos" ou "criadouros"

# Executa os scripts passando o tipo como argumento
subprocess.run(["python", "dados_APAC.py", tipo])
subprocess.run(["python", "dados_INMET.py", tipo])
subprocess.run(["python", "conjuntos_predicao.py", tipo])
subprocess.run(["python", "interpolacao_conjunto_predicao.py"])
