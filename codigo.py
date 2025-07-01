import pandas as pd
import numpy as np

print('Coletando dados para análise...')

CAMINHO_ARQUIVO_1 = './BaseDP.csv'
df_serie_1 = pd.read_csv(CAMINHO_ARQUIVO_1 , sep=';', encoding='iso-8859-1')
df_serie_1.columns = [col.strip().replace('ï»¿cod_ocorrencia', 'cod_ocorrencia') for col in df_serie_1.columns]
print(df_serie_1)

CAMINHO_ARQUIVO_2 = './BaseDP_Roubo_Coletivo.csv'
df_serie_2 = pd.read_csv(CAMINHO_ARQUIVO_2 , sep=';', encoding='iso-8859-1')
df_serie_2.columns = [col.strip().replace('ï»¿cod_ocorrencia', 'cod_ocorrencia') for col in df_serie_2.columns]
print(df_serie_2)

df_roubo_coletivo = pd.merge(df_serie_1, df_serie_2, on='cod_ocorrencia')  # on='coluna no dataframe'

print(df_roubo_coletivo)

array_roubo_coletivo = np.array(df_roubo_coletivo)
