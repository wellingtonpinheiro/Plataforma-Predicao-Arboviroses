import json
import subprocess
import os

def executar_pipeline(tipo, ano, bimestre):
    try:
        # Atualizar o config.json
        config = {
            "tipo_analise": tipo,
            "ano": ano,
            "bimestre": bimestre
        }
        caminho_config = os.path.join('INTERPOLAÇÃO/config.json') 
        with open(caminho_config, 'w') as f:
            json.dump(config, f)

        # Executar os scripts em sequência
        subprocess.run(['python', 'INTERPOLAÇÃO/dados_APAC.py', tipo], check=True)
        subprocess.run(['python', 'INTERPOLAÇÃO/dados_INMET.py', tipo], check=True)
        subprocess.run(['python', 'INTERPOLAÇÃO/conjuntos_predicao.py', tipo], check=True)
        subprocess.run(['python', 'INTERPOLAÇÃO/interpolacao_conjunto_predicao.py'], check=True)

        return True, None  # Sucesso

    except subprocess.CalledProcessError as e:
        return False, f"Erro ao executar pipeline: {str(e)}"
