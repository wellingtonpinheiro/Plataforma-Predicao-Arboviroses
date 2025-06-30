import os
from django.conf import settings

def executar_pipeline(tipo='casos', ano=2014, bimestre=1):
    try:
        base_dir = settings.BASE_DIR
        caminho_png = os.path.join(base_dir, 'static', 'maps', 'predicao_recife.png')

        if not os.path.exists(caminho_png):
            raise FileNotFoundError(f"Arquivo PNG não encontrado: {caminho_png}")

        return True, None

    except Exception as e:
        return False, str(e)
