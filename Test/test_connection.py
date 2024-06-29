import unittest
from unittest.mock import patch
import requests
import pandas as pd
from import_cotahistA2024 import DataLoader, DataProcessor, \
    ModelTrainer


class TestDataLoader(unittest.TestCase):
    @patch('requests.get')
    def test_load_data_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {'_id': '1', 'CODNEG': 'LWSA3', 'PRE-ABE': 10.0, 'PRE-ULT': 12.0, 'PRE-OFV': 11.0, 'PREMED': 11.5,
             'VOLT-TOT': 1000, 'DATA_PREGAO': '2023-06-28'},
            {'_id': '2', 'CODNEG': 'PETR4', 'PRE-ABE': 10.0, 'PRE-ULT': 12.0, 'PRE-OFV': 11.0, 'PREMED': 11.5,
             'VOLT-TOT': 1000, 'DATA_PREGAO': '2023-06-28'}

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
        self.assertEqual(len(data_loader.dados), 2)
        self.assertEqual(data_loader.dados.iloc[0]['CODNEG'], 'LWSA3')
        self.assertEqual(data_loader.dados.iloc[1]['CODNEG'], 'PETR4')


class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        data = [
            {'CODNEG': 'LWSA3', 'PRE-ABE': 10.0, 'PRE-ULT': 12.0, 'PRE-OFV': 11.0, 'PREMED': 11.5, 'VOLT-TOT': 1000,
             'DATA_PREGAO': '2023-06-28'},

        ]
        self.dados = pd.DataFrame(data)

    def test_filter_data_success(self):
        data_processor = DataProcessor(self.dados)
        data_processor.filter_data('LWSA3')

        self.assertIsNotNone(data_processor.dados_filtrados)
        self.assertEqual(len(data_processor.dados_filtrados), 1)

    def test_calculate_dif_cotacao(self):
        data_processor = DataProcessor(self.dados)
        data_processor.filter_data('LWSA3')
        data_processor.calculate_dif_cotacao()

        self.assertIn('DIF_COTACAO', data_processor.dados.columns)
        self.assertEqual(data_processor.dados['DIF_COTACAO'].iloc[0], 33.5)


class TestModelTrainer(unittest.TestCase):
    def setUp(self):
        data = [
            {'CODNEG': 'LWSA3', 'PRE-ABE': 10.0, 'PRE-ULT': 12.0, 'PRE-OFV': 11.0, 'PREMED': 11.5, 'VOLT-TOT': 1000,
             'DATA_PREGAO': '2023-06-28'},
            {'CODNEG': 'LWSA3', 'PRE-ABE': 11.0, 'PRE-ULT': 13.0, 'PRE-OFV': 12.0, 'PREMED': 12.5, 'VOLT-TOT': 1100,
             'DATA_PREGAO': '2023-06-29'},
            # Adicione mais dados de teste conforme necessário
        ]
        self.dados_filtrados = pd.DataFrame(data)
        self.variaveis_filtradas = ['VOLT-TOT', 'PREMED', 'PRE-OFV', 'PRE-ULT', 'PRE-ABE']

    def test_split_data(self):
        model_trainer = ModelTrainer(self.dados_filtrados, self.variaveis_filtradas)
        model_trainer.split_data()

        self.assertIsNotNone(model_trainer.X_train)
        self.assertIsNotNone(model_trainer.X_test)
        self.assertIsNotNone(model_trainer.y_train)
        self.assertIsNotNone(model_trainer.y_test)

    def test_train_model(self):
        model_trainer = ModelTrainer(self.dados_filtrados, self.variaveis_filtradas)
        model_trainer.split_data()
        model_trainer.train_model()

        self.assertTrue(hasattr(model_trainer.model, "tree_"))

    def test_predict(self):
        model_trainer = ModelTrainer(self.dados_filtrados, self.variaveis_filtradas)
        model_trainer.split_data()
        model_trainer.train_model()

        previsoes = model_trainer.predict()
        self.assertEqual(len(previsoes), len(model_trainer.X_test))

    def test_calculate_correlation(self):
        model_trainer = ModelTrainer(self.dados_filtrados, self.variaveis_filtradas)
        correlation = model_trainer.calculate_correlation()

        self.assertIsInstance(correlation, float)


if __name__ == '__main__':
    unittest.main()
