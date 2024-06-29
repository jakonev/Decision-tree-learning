import unittest
import pandas as pd
from import_cotahistA2024 import ModelTrainer

class TestModelTrainer(unittest.TestCase):
    def setUp(self):
        data = [
            {'CODNEG': 'LWSA3', 'PRE-ABE': 10.0, 'PRE-ULT': 12.0, 'PRE-OFV': 11.0, 'PREMED': 11.5, 'VOLT-TOT': 1000, 'DATA_PREGAO': '2023-06-28'},
            {'CODNEG': 'LWSA3', 'PRE-ABE': 11.0, 'PRE-ULT': 13.0, 'PRE-OFV': 12.0, 'PREMED': 12.5, 'VOLT-TOT': 1100, 'DATA_PREGAO': '2023-06-29'},
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
