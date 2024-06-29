import unittest
from unittest.mock import patch
import requests
import pandas as pd
from statistic import DataLoader, DataProcessor

class TestDataLoader(unittest.TestCase):
    @patch('requests.get')
    def test_load_data_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {'_id': '1', 'CODNEG': 'CVCB3', 'PRE-ABE': 10.0, 'PRE-ULT': 12.0, 'PRE-OFV': 11.0, 'PREMED': 11.5,
             'VOLT-TOT': 1000, 'DATA_PREGAO': '2023-06-28T00:00:00Z'},
            # Adicione mais dados de teste conforme necessário
        ]

        url = "https://cotahist-2f8e.restdb.io/rest/cota-hist"
        headers = {
            'content-type': "application/json",
            'x-apikey': "a78a2fe211a7547f5fc7f323bf8ed3a99651a",
            'cache-control': "no-cache"
        }
        params = {'_id': '', 'CODNEG': '', 'PRE-ABE': '', 'PRE-ULT': '', 'PRE-OFV': '', 'PREMED': '', 'VOLT-TOT': '',
                  'DATA_PREGAO': ''}

        data_loader = DataLoader(url, headers, params)
        data_loader.load_data()

        self.assertIsNotNone(data_loader.dados)
        self.assertEqual(len(data_loader.dados), 1)
        self.assertEqual(data_loader.dados.iloc[0]['CODNEG'], 'CVCB3')


class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        data = [
            {'CODNEG': 'CVCB3', 'PRE-ABE': 10.0, 'PRE-ULT': 12.0, 'PRE-OFV': 11.0, 'PREMED': 11.5, 'VOLT-TOT': 1000,
             'DATA_PREGAO': ''},

        ]
        self.dados = pd.DataFrame(data)

    def test_filter_data_success(self):
        data_processor = DataProcessor(self.dados)
        data_processor.filter_data('CVCB3')

        self.assertIsNotNone(data_processor.dados_filtrados)
        self.assertEqual(len(data_processor.dados_filtrados), 1)

    # def test_calcula_statistic(self):
    #     data_processor = DataProcessor(self.dados)
    #     data_processor.filter_data('CVCB3')
    #     data_atualizacao = '2023-06-28 00:00:00'
    #     resultado = data_processor.calcula_statistic(atualizacao=data_atualizacao, preAbert=None, preUltm=None,
    #                                                  preMed=None)
    #
    #     self.assertIn('Atualizado em 2023-06-28 00:00:00', resultado)
    #     self.assertIn('Preco Abertura Min: 10.0', resultado)
    #     self.assertIn('Preco Media Minimo: 11.5', resultado)
    #     self.assertIn('Preco Ultimo Max: 12.0', resultado)
    #     self.assertIn('Preco Med: 11.5', resultado)


if __name__ == '__main__':
    unittest.main()
