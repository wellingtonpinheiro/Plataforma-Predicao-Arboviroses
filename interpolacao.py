import subprocess
import os


def Interpolation(folder1, folder2, path):
    """
    :param folder2: pasta para salvar os mapas interpolados
    :param folder1: pasta com os arquivos ".csv" para interpolação
    :return:
    """
    # definir os comandos e argumentos que serão passados para o prompt de comando
    command = path
    path2script = os.path.join(os.getcwd(), 'interpolation.R')

    # build process command
    cmd = [command, '--vanilla', path2script, folder1, folder2]

    # check_output will run to the command and store result
    subprocess.call(cmd, shell=True)
