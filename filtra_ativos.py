import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeRegressor


dados = pd.read_csv('data_filtro.csv')
CODNEG_filtrado = 'RAIZ4'
dados_filtrados = dados.query(f'CODNEG == "{CODNEG_filtrado}"')

DIF_PRECO = dados['PRE-ABE']
dados.loc[:, 'DIF_COTACAO'] = (dados_filtrados['PRE-ABE'] + dados_filtrados['PRE-ULT'].min() + dados_filtrados['PREMED']) / 3

# Codificar variáveis categóricas caso inclua codnego fracionado
label_encoder = LabelEncoder()
dados['CODNEG'] = label_encoder.fit_transform(dados['CODNEG'])


variaveis_filtradas = ['VOLT-TOTAL', 'PREMED', 'PRE-OFV', 'PRE-ULT', 'PRE-ABE']

X = dados[variaveis_filtradas]
y = dados['PRE-ULT']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=12, random_state=42)

modelo = DecisionTreeRegressor(random_state=42)
modelo.fit(X_train, y_train)

previsoes = modelo.predict(X_test)

correlacao_abertura = dados['PREMED'].corr(dados['PRE-ULT'])
for i, predicao in enumerate(previsoes):
    print(f"Resultado da previsão {i+1}: {predicao}")

print(f"Correlação PREMED e Último Preço: {correlacao_abertura:,.4f}")


