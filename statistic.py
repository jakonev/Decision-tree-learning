import pandas as pd
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

    def calcula_statistic(self, preAbert, preUltm, preMed):
        preAbert = self.dados_filtrados['PRE-ABE'].min()
        preUltm = self.dados_filtrados['PRE-ULT'].max()
        preMed = self.dados_filtrados['PREMED'].median()

        return print(f'Preco Abertura Min: {preAbert} | Preco Ultimo Max: {preUltm} | Preco Med: {preMed}')

def main():
    file_path = 'data_filtro.csv'
    codneg_filtrado = 'RAIZ4'
    data_loader = DataLoader(file_path)
    data_loader.load_data()
    data_processor = DataProcessor(data_loader.dados)

    try:
        data_processor.filter_data(codneg_filtrado)
        data_processor.calcula_statistic(preAbert=None, preUltm=None, preMed=None)

    except ValueError as e:
        print(e)
        return


if __name__ == "__main__":
    main()
