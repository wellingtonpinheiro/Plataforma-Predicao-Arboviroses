
# Plataforma-Predicao-Arboviroses

# Passo a Passo para Rodar o Código

### Passo 1 
Caso não tenha ainda a biblioteca `pyenv` instalada roder o comando abaixo no seu editor de código.
> Esta biblioteca é responsável por criar um ambiente virtual e armazenar as dependências do projeto que estarão no arquivo `requirements.txt`

```
pip install pyenv
```

### Passo 2 - Criar o seu ambiente virtual.
Por padrão o ambiente virtual está com o nome `myenv`, mas caso queria usar outro nome certifique de que o nome da pasta esteja presente no arquivo `.gitignore`)
```
 python -m venv myenv
```
### Passo 3 - Ativar o ambiente virtual
Toda vez que for iniciado o terminal é necessário realizar esse comando de ativar o *myenv* para que seja inicializado as bibliotecas necessárias para o projeto ser executado. 
```
myenv\Scripts\activate
```
### Passo 4 - Intaslar dependências do projeto
🟥 ATENÇÃO!🟥

Esse passo deve ser realizado com o `myenv` ativado, para que as dependências fiquem no ambiente virtual e não na sua máquina. Assim padronizando todas as versões das bibliotecas que estão sendo usadas no projeto.

**Esse passo só deve ser realizado uma única vez ou ao for adicionado uma biblioteca nova no arquivo** `requirements.txt` (arquivo que contém todas as dependências do projeto)
```
pip install -r requirements.txt
```

### Passo 5 - Executar o manage.py

Entre na pasta do projeto
```
cd plataforma
```
Depois rode o `manage.py`
```
python manage.py runserver
```

