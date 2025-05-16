import subprocess
import os


def Interpolation(folder1, folder2, rscript_path):
    """
    Executa o script R de interpolação com os diretórios de entrada e saída corrigidos.

    :param folder1: pasta com os arquivos .csv para interpolação (entrada)
    :param folder2: pasta para salvar os arquivos interpolados (saída)
    :param rscript_path: caminho para o executável Rscript (ex: "C:/Program Files/R/R-4.3.2/bin/Rscript.exe")
    """

    # Caminho absoluto do script R
    path_to_script = os.path.abspath('interpolation.R')

    # Caminhos absolutos e normalizados para o R (com barra normal '/')
    input_dir  = os.path.abspath(folder1).replace("\\", "/")
    output_dir = os.path.abspath(folder2).replace("\\", "/")

    # Comando para chamar o Rscript
    cmd = [rscript_path, '--vanilla', path_to_script, input_dir, output_dir]

    # Executa o comando
    subprocess.call(cmd)
