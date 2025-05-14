

from zipfile import ZipFile
from os import getcwd, listdir, path, makedirs
import pathlib
from time import sleep


def get_filename(url):
    return path.basename(url)


def extract(station, final_folder, year):
    # listando os arquivos .zip do diretório
    zip_files = [file for file in listdir(getcwd()) if pathlib.Path(file).suffix == ".zip"]
    zip_files = [file for file in zip_files if year in file]

    print(zip_files)

    # Criando uma pasta para colocar os dados do INMET
    makedirs(path.join(getcwd(), final_folder), exist_ok=True)

    # lista de arquivos da pasta do INMET para não repetir o processo de extraçao dos arquivos
    dados_INMET_files = [file for file in listdir(final_folder)]

    # extraindo os arquivos que estão nas pastas zipadas
    for folder in zip_files:
        sleep(1.5)
        #zip = ZipFile(folder)
        list_files = ZipFile(folder).namelist()

        # extraíndo apenas os arquivos da estação automática do Recife
        index_ = [file for file in list_files if station in file]

        for file in index_:
            if get_filename(file) not in dados_INMET_files:
                print("Extraindo os arquivos de Recife na pasta {}".format(folder))
                f = ZipFile(folder).open(file)  # extrai o arquivo dentro de uma pasta zipada

                # salva o arquivo extraido
                content = f.read()
                f = open(path.join(final_folder, get_filename(file)), 'wb')
                f.write(content)
                f.close()
            else:
                print("O arquivo já existe na pasta de 'dados brutos INMET!!!!'")
