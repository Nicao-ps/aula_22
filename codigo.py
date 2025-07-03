from sqlalchemy import create_engine
import pandas as pd
import numpy as np


entrada = input('\nInforme a entrada de dados [csv / sql]: ')

try:
	if entrada == 'csv':
		CAMINHO_ARQUIVO_1 = './BaseDP.csv'
		df_serie_1 = pd.read_csv(CAMINHO_ARQUIVO_1, sep=';', encoding='utf-8')
		df_serie_1.columns = [col.strip().replace('ï»¿cod_ocorrencia', 'cod_ocorrencia') for col in df_serie_1.columns]
		CAMINHO_ARQUIVO_2 = './BaseDP_Roubo_Coletivo.csv'
		df_serie_2 = pd.read_csv(CAMINHO_ARQUIVO_2, sep=';', encoding='utf-8')
		df_serie_2.columns = [col.strip().replace('ï»¿cod_ocorrencia', 'cod_ocorrencia') for col in df_serie_2.columns]

	elif entrada == 'sql':
		host = 'localhost'
		user = 'root'
		password = ''
		database = 'roubo_coletivo'
		engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')
		df_serie_1 = pd.read_sql_query('SELECT * FROM basedp', engine)
		df_serie_2 = pd.read_sql_query('SELECT * FROM basedp_roubo_coletivo', engine)



except Exception as e:
	print(f'Erro! {e}')
	exit()

print('\nColetando dados para análise...\n')
df_novo = pd.merge(df_serie_1, df_serie_2, on='cod_ocorrencia')  # on='coluna no dataframe'
df_novo_filtrado = df_novo[(df_novo['ano'] >= 2022) & (df_novo['ano'] <= 2023)]
print(df_novo_filtrado)

df_roubo_coletivo = df_novo_filtrado.groupby('munic').sum(['roubo_em_coletivo']).reset_index()

array_roubo_coletivo = np.array(df_roubo_coletivo['roubo_em_coletivo'])

media = np.mean(array_roubo_coletivo)
print(media)

mediana = np.median(array_roubo_coletivo)
print(mediana)

# quantis da serie
print('Quantis:\n')
list_q = []
qtt_q = int(input('Quantis utilizados para análise: '))
print('')
for i in range(qtt_q):
	q = float(input(f'Informe o q{i + 1}: '))
	list_q.append(q)
print('')
for i in range(qtt_q):
	print(f'q{i + 1} = {np.quantile(array_roubo_coletivo, list_q[i], method="weibull"):.2f}')
print('')

# intervalo interquantil
iqr = np.quantile(array_roubo_coletivo, list_q[qtt_q - 1], method="weibull") - np.quantile(array_roubo_coletivo, list_q[0], method="weibull")
print(f'Intervalo interquantil: {iqr:.2f}')

print('\nLimites:\n')

# limite superior da serie
mayor_limit = np.quantile(array_roubo_coletivo, list_q[qtt_q - 1], method="weibull") + (1.5 * iqr)
print(f'Limite superior: {mayor_limit:.2f}')

# limite inferior da serie
minor_limit = np.quantile(array_roubo_coletivo, list_q[0], method="weibull") - (1.5 * iqr)
print(f'Limite inferior: {minor_limit:.2f}')

# maiores da serie
print('\nMaiores:\n')
df_roubo_coletivo_maiores = df_roubo_coletivo[df_roubo_coletivo['roubo_em_coletivo'] > np.quantile(array_roubo_coletivo, list_q[qtt_q - 1], method="weibull")]
print(df_roubo_coletivo_maiores.sort_values(by='roubo_em_coletivo', ascending=False))

# menores da serie
print('\nMenores:\n')
df_roubo_coletivo_menores = df_roubo_coletivo[df_roubo_coletivo['roubo_em_coletivo'] < np.quantile(array_roubo_coletivo, list_q[0], method="weibull")]
print(df_roubo_coletivo_menores.sort_values(by='roubo_em_coletivo', ascending=True))

print('\nOutliers:\n')
	
# outliers superiores da serie
df_roubo_coletivo_maiores_outliers = df_roubo_coletivo[df_roubo_coletivo['roubo_em_coletivo'] > mayor_limit]
if len(df_roubo_coletivo_maiores_outliers) == 0:
	print('\nNão existe outliers superiores!')
else:
	print('\nOutliers Superiores:\n')
	print(df_roubo_coletivo_maiores_outliers.sort_values(by='roubo_em_coletivo', ascending=False))

# outliers inferiores da serie
df_roubo_coletivo_menores_outliers = df_roubo_coletivo[df_roubo_coletivo['roubo_em_coletivo'] < minor_limit]

if len(df_roubo_coletivo_menores_outliers) == 0:
	print('\nNão existem outliers inferiores!')
else:
	print('\nOutliers Inferiores:\n')
	print(df_roubo_coletivo_menores_outliers.sort_values(by='roubo_em_coletivo', ascending=True))

try:
	import matplotlib.pyplot as plt
	


	plt.tight_layout()
	plt.show()

except Exception as e:
	print(f'Erro ao plotar o gráfico: {e}')
