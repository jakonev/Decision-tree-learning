from datetime import datetime, timezone

import pandas as pd
import requests


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

    def calcula_statistic(self, atualizacao, preAbert, preUltm, preMed):
        preAbert = self.dados_filtrados['PRE-ABE'].min()
        preUltm = self.dados_filtrados['PRE-ULT'].max()
        preMed = self.dados_filtrados['PREMED'].median()



        return print(f'| Atualizado em {atualizacao}| Preco Abertura Min: {preAbert} | Preco Ultimo Max: {preUltm} | Preco Med: {preMed}')


def calculos():
    # Parâmetros da API NAO ESTRAGAR A BASE DO REST
    # DO NOT CHANGE THE GET API METHOD AND THE BASE PLEASE
    url = "https://cotahist-2f8e.restdb.io/rest/cota-hist"
    headers = {
        'content-type': "application/json",
        'x-apikey': "a78a2fe211a7547f5fc7f323bf8ed3a99651a",
        'cache-control': "no-cache"
    }
    params = {'_id': type, 'CODNEG': '', 'PRE-ABE': float, 'PRE-ULT': float, 'PRE-OFV': float, 'PREMED': float, 'VOLT-TOT': float,
              'DATA_PREGAO': datetime.timetz}

    # Parâmetros de filtro e variáveis
    codneg_filtrado = 'PETR3'
    variaveis_filtradas = ['VOLTOT', 'PREMED', 'PRE-OFV', 'PRE-ULT', 'PRE-ABE']

    # Carregar dados
    data_loader = DataLoader(url, headers, params)
    data_loader.load_data()

    # Processar dados
    data_processor = DataProcessor(data_loader.dados)

    try:
        data_processor.filter_data(codneg_filtrado)
        data_atualizacao = data_processor.dados_filtrados['DATA_PREGAO'].max()
        data_processor.calcula_statistic(atualizacao=data_atualizacao, preAbert=None, preUltm=None, preMed=None)

    except ValueError as e:
        print(e)
        return


if __name__ == "__main__":
    calculos()
