import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor


class DataLoader:
    def __init__(self, url, headers, params):
        self.url = url
        self.headers = headers
        self.params = params
        self.dados = None

    def load_data(self):
        response = requests.get(self.url, headers=self.headers, params=self.params)
        if response.status_code == 200:
            self.dados = pd.DataFrame(response.json())
        else:
            response.raise_for_status()


class DataProcessor:
    def __init__(self, dados):
        self.dados = dados
        self.dados_filtrados = None

    def filter_data(self, codneg_filtrado):
        self.dados_filtrados = self.dados.query(f'CODNEG == "{codneg_filtrado}"')
        if self.dados_filtrados.empty:
            raise ValueError(f"Não há dados disponíveis para CODNEG {codneg_filtrado}")

    def calculate_dif_cotacao(self):
        self.dados['DIF_COTACAO'] = (
                self.dados_filtrados['PRE-ABE'].min() +
                self.dados_filtrados['PRE-ULT'].min() +
                self.dados_filtrados['PREMED'].min()
        )


class ModelTrainer:
    def __init__(self, dados_filtrados, variaveis_filtradas, target='PRE-OFV'):
        self.dados_filtrados = dados_filtrados
        self.variaveis_filtradas = variaveis_filtradas
        self.target = target
        self.model = DecisionTreeRegressor(random_state=42)
        self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None

    def split_data(self):
        X = self.dados_filtrados[self.variaveis_filtradas]
        y = self.dados_filtrados[self.target]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    def train_model(self):
        self.model.fit(self.X_train, self.y_train)

    def predict(self):
        return self.model.predict(self.X_test)

    def calculate_correlation(self):
        return self.dados_filtrados['PREMED'].corr(self.dados_filtrados['PRE-ULT'])


class Plotter:
    def __init__(self, dados_filtrados, variaveis_filtradas, predicoes, codneg_filtrado):
        self.dados_filtrados = dados_filtrados
        self.variaveis_filtradas = variaveis_filtradas
        self.predicoes = predicoes
        self.codneg_filtrado = codneg_filtrado

    def plot_histogram(self):
        plt.figure(figsize=(10, 6))
        sns.histplot(self.dados_filtrados[self.variaveis_filtradas], x="PRE-ULT", hue=self.predicoes, element="step",
                     kde=True)
        plt.title(f'{self.codneg_filtrado}')
        plt.xlabel(f'{self.codneg_filtrado}')
        plt.ylabel('Frequência')
        plt.show()


def resultados():
    # Parâmetros da API NAO ESTRAGAR A BASE DO REST
    # DO NOT CHANGE THE GET API METHOD AND THE BASE PLEASE
    url = "https://cotahist-2f8e.restdb.io/rest/cota-hist"
    headers = {
        'content-type': "application/json",
        'x-apikey': "a78a2fe211a7547f5fc7f323bf8ed3a99651a",
        'cache-control': "no-cache"
    }
    params = {'_id': type, 'CODNEG': '', 'PRE-ABE': float, 'PRE-ULT': float, 'PRE-OFV': float, 'PREMED': float, 'VOLT-TOT': float,
              'DATA_PREGAO': ''}

    # Parâmetros de filtro e variáveis
    codneg_filtrado = 'HBSA3'
    variaveis_filtradas = ['VOLTOT', 'PREMED', 'PRE-OFV', 'PRE-ULT', 'PRE-ABE']

    # Carregar dados
    data_loader = DataLoader(url, headers, params)
    data_loader.load_data()

    # Processar dados
    data_processor = DataProcessor(data_loader.dados)
    try:
        data_processor.filter_data(codneg_filtrado)
        data_processor.calculate_dif_cotacao()
    except ValueError as e:
        print(e)
        return

    # Treinar modelo
    model_trainer = ModelTrainer(data_processor.dados_filtrados, variaveis_filtradas)
    model_trainer.split_data()
    model_trainer.train_model()

    # Fazer previsões e calcular correlação
    previsoes = model_trainer.predict()
    correlacao_abertura = model_trainer.calculate_correlation()

    for i, predicao in enumerate(previsoes):
        print(f"Resultado da previsão {i + 1}: {predicao}")

    print(f"Correlação PREMED e Último Preço: {correlacao_abertura:,.4f}")

    # Plotar resultados
    plt.figure(figsize=(10, 6))
    sns.histplot(data_processor.dados_filtrados, x='PREMED', hue=predicao, bins=20, kde=True)
    plt.title('PRECO MEDIO')
    plt.xlabel(f'{codneg_filtrado}')
    plt.ylabel('Frequência')
    plt.show()


if __name__ == "__main__":
    resultados()
