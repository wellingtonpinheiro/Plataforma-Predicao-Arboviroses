import json
import subprocess

# Carrega o config.json
with open("config.json", "r") as f:
    config = json.load(f)

subprocess.run(["python", "dados_APAC.py"])
subprocess.run(["python", "dados_INMET.py"])
subprocess.run(["python", "contagem_casos.py"])
subprocess.run(["python", "conjuntos_predicao.py"])
subprocess.run(["python", "interpolacao_conjunto_predicao.py"])