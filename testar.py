import joblib
import numpy as np
from sklearn.pipeline import Pipeline

# Carrega o modelo
modelo = joblib.load(r'plataformaapp\modelos\modelo_rf_casos_2014_1.pkl')  # Substitua pelo seu arquivo

# Se for um Pipeline, precisamos ver os steps
if isinstance(modelo, Pipeline):
    # Verifica o pré-processador (normalmente o primeiro step)
    preprocessor = modelo.steps[0][1]
    
    # Se for um ColumnTransformer, podemos ver as colunas
    if hasattr(preprocessor, 'transformers'):
        for name, transformer, columns in preprocessor.transformers:
            print(f"Transformador: {name}")
            print(f"Colunas: {columns}")
            print("------")
    
    # Pega o estimador final (normalmente o último step)
    estimator = modelo.steps[-1][1]
else:
    estimator = modelo

# Verifica os feature names se disponível
if hasattr(estimator, 'feature_names_in_'):
    print("Features esperadas pelo modelo:")
    print(estimator.feature_names_in_)
    print(f"Total: {len(estimator.feature_names_in_)} features")
else:
    print("O modelo não tem feature names registrados. Você precisará:")
    print("1. Verificar como o modelo foi treinado originalmente")
    print("2. Ou recriar o DataFrame com as mesmas colunas usadas no treino")