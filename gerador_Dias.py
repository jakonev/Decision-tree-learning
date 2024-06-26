import datetime


class GeradorPrevisao:
    @staticmethod
    def obter_previsao_dias_mes():
        # Obter a data atual
        data_atual = datetime.date.today()

        # Obter o número total de dias no mês atual
        ultimo_dia_mes = data_atual.day

        # Criar a lista de dias do mês até o dia atual
        PREVISAO = list(range(1, ultimo_dia_mes))

        return PREVISAO
