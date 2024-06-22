import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeRegressor

# Carregar os dados
dados = pd.read_csv('data.csv')

# Converter a coluna 'data_compra' para datetime
dados['DATA_PREGAO'] = pd.to_datetime(dados['DATA_PREGAO'])

# Media de precos calculados
DIF_PRECO = dados['PRE-ABE']
dados['DIF_COTACAO'] = (dados['PRE-ABE'] + dados['PRE-ULT'].min() + dados['PREMED']) / 3

# Codificar variáveis categóricas caso inclua codnego fracionado
label_encoder = LabelEncoder()
dados['CODNEG'] = label_encoder.fit_transform(dados['CODNEG'])


# Selecionar variáveis relevantes, opcional alterar a vontade
variaveis = ['VOLT-TOTAL', 'PREMED', 'PRE-OFV', 'PRE-ULT', 'PRE-ABE']

# Dividir os dados em conjunto de treinamento e teste
X = dados[variaveis]
y = dados['PRE-ULT']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

modelo = DecisionTreeRegressor(random_state=42)
modelo.fit(X_train, y_train)

# Fazer previsões no conjunto de teste
previsoes = modelo.predict(X_test)

# Avaliar a precisão do modelo

# Calcular a correlação entre o número de dias desde a data de referência e a variável
correlacao_abertura = dados['PREMED'].corr(dados['PRE-ULT'])
for i, predicao in enumerate(previsoes):
    print(f"Resultado da previsão {i+1}: {predicao}")

# Visualizar a correlação
print(f"Correlação PREMED e Oferta Venda: {correlacao_abertura:,.4f}")

plt.figure(figsize=(10, 6))
sns.histplot(data=dados[variaveis], x='PREMED', hue=predicao, bins=20, kde=True)
plt.title('PRECO MEDIO')
plt.xlabel('COMPRA BEEF3')
plt.ylabel('Frequência')
plt.show()

PREVISAO = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]

beef3 = previsoes

# Criar figura e eixos
fig, ax = plt.subplots()
ax.plot(PREVISAO, beef3, label='BEEF3')

ax.set_xlabel('Previsões')
ax.set_ylabel('Preço(R$)')
ax.legend()

# Exibir o gráfico pronto
plt.show()