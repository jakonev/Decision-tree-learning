import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeRegressor


dados = pd.read_csv('data_filtro.csv')
CODNEG_filtrado = 'PCAR3'
dados_filtrados = dados.query(f'CODNEG == "{CODNEG_filtrado}"')

DIF_PRECO = dados_filtrados['PRE-ABE']
dados['DIF_COTACAO'] = (dados_filtrados['PRE-ABE'].median() + dados_filtrados['PRE-ULT'].max() + dados_filtrados['PREMED'].median())

# dados_filtrados['DIF_COTACAO'] = (dados_filtrados['PRE-ABE'] + dados_filtrados['PRE-ULT'] + dados_filtrados['PREMED']) / 3
variaveis_filtradas = ['VOLT-TOT', 'PREMED', 'PRE-OFV', 'PRE-ULT', 'PRE-ABE']

if dados_filtrados.empty:
    print(f"Não há dados disponíveis para CODNEG {CODNEG_filtrado}")
else:
    # Dividir os dados filtrados em conjunto de treinamento e teste
    X = dados_filtrados[variaveis_filtradas]
    y = dados_filtrados['PRE-ULT']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Treinar o modelo de regressão
    modelo = DecisionTreeRegressor(random_state=42)
    modelo.fit(X_train, y_train)

    # Fazer previsões no conjunto de teste
    previsoes = modelo.predict(X_test)

    # Avaliar a precisão do modelo

    # Calcular a correlação entre a variável PREMED e PRE-ULT
    correlacao_abertura = dados_filtrados['PREMED'].corr(dados_filtrados['PRE-ULT'])
    for i, predicao in enumerate(previsoes):
        print(f"Resultado da previsão {i+1}: {predicao}")

    # Visualizar a correlação
    print(f"Correlação PREMED e Último Preço: {correlacao_abertura:,.4f}")

    print(X_train)