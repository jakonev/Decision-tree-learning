import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor


class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.dados = None

    def load_data(self):
        self.dados = pd.read_csv(self.file_path)


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
                self.dados_filtrados['PREMED']
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


def main():
    # Parâmetros
    file_path = 'data_filtro.csv'

    codneg_filtrado = 'RAIZ4'
    variaveis_filtradas = ['VOLT-TOT', 'PREMED', 'PRE-OFV', 'PRE-ULT', 'PRE-ABE']

    # Carregar dados
    data_loader = DataLoader(file_path)
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
    # plt.figure(figsize=(10, 6))
    # sns.histplot(data=data_processor.dados_filtrados, x='PREMED', hue=predicao, bins=20, kde=True)
    # plt.title('PRECO MEDIO')
    # plt.xlabel(f'{codneg_filtrado}')
    # plt.ylabel('Frequência')
    # plt.show()

if __name__ == "__main__":
    main()
