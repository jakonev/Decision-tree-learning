import datetime


class GeradorPrevisao:
    @staticmethod
    def obter_previsao_dias_mes():
        # Obter a data atual
        data_atual = datetime.date.today()
        ultimo_dia_mes = data_atual.day
        # AJUSTAR PARA ATUALIZACAO NO FINAL DE SEMANA
        PREVISAO = list(range(1, ultimo_dia_mes - 3))

        return PREVISAO
