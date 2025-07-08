from sqlalchemy import create_engine
import pandas as pd
import numpy as np


print('\n\n'+'Bem vindo analista em formação!'+'\n')


entrada = input('\nInforme o formato desejado para os dados de entrada [csv / sql]: ')


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
		df_serie_1.columns = [col.strip().replace('ï»¿cod_ocorrencia', 'cod_ocorrencia') for col in df_serie_1.columns]
		df_serie_2 = pd.read_sql_query('SELECT * FROM basedp_roubo_coletivo', engine)
		df_serie_2.columns = [col.strip().replace('ï»¿cod_ocorrencia', 'cod_ocorrencia') for col in df_serie_2.columns]

except Exception as e:
	print(f'Erro! {e}')
	exit()


print('\n\n'+'Coletando dados para análise...'+'\n')


df_novo = pd.merge(df_serie_1, df_serie_2, on='cod_ocorrencia')  # on='coluna no dataframe'
df_novo_filtrado = df_novo[(df_novo['ano'] >= 2022) & (df_novo['ano'] <= 2023)]
filtra_col = ['munic', 'roubo_em_coletivo']
df_novo_filtrado = df_novo_filtrado[filtra_col].groupby('munic').sum(['roubo_em_coletivo']).sort_values(by='munic', ascending=True).sort_values(by='roubo_em_coletivo', ascending=False).reset_index()
df_roubo_coletivo = df_novo_filtrado


print('\n'+('-'*73))
print('Análise dos Roubos em Coletivo nos anos de 2022 e de 2023 no Estado do RJ')
print(('-'*73)+'\n')


print(df_roubo_coletivo)


array_roubo_coletivo = np.array(df_roubo_coletivo['roubo_em_coletivo'])


# medidas de tendência central da série
print('\n'+('-'*28))
print('Medidas de Tendência Central')
print(('-'*28)+'\n')

media = np.mean(array_roubo_coletivo)
print(f'Média de roubo em coletivos: {media:.2f}')

mediana = np.median(array_roubo_coletivo)
print(f'Mediana de roubo em coletivos: {mediana:.2f}')


# medidas de posição da série
print('\n'+('-'*18))
print('Medidas de Posição')
print(('-'*18)+'\n')


# quantis da serie
print(('-'*7))
print('Quantis')
print(('-'*7))

list_q = []
qtt_q = int(input('\n'+'Quantis utilizados para análise: '))
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


# limites da serie
print('\n'+('-'*7))
print('Limites')
print(('-'*7)+'\n')

# limite superior da serie
mayor_limit = np.quantile(array_roubo_coletivo, list_q[qtt_q - 1], method="weibull") + (1.5 * iqr)
print(f'Limite superior: {mayor_limit:.2f}')

# limite inferior da serie
minor_limit = np.quantile(array_roubo_coletivo, list_q[0], method="weibull") - (1.5 * iqr)
print(f'Limite inferior: {minor_limit:.2f}')

input('\nImprimir maiores e menores? [s/n]: ')

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
