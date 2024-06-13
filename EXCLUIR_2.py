import datetime

import pandas as pd
import requests

import requests
# informe = input('Escreva o local C: ')
# excluido = f'Todos os dados de: --- {informe} --- Foram excluídos com Sucesso !!'
#
# print(excluido)

url = "https://cotahist-2f8e.restdb.io/rest/cota-hist"
headers = {
        'content-type': "application/json",
        'x-apikey': "a78a2fe211a7547f5fc7f323bf8ed3a99651a",
        'cache-control': "no-cache"
    }
params = {'_id': type, 'CODNEG': '', 'PRE-ABE': float, 'PRE-ULT': float, 'PRE-OFV': float, 'PREMED': float, 'VOLT-TOT': float,
              'DATA_PREGAO': datetime.timezone}

response = requests.get(url, headers=headers, params=params)
dados = pd.DataFrame(response.json())
atualizacao = (dados['DATA_PREGAO'].max())

print(atualizacao)
