import datetime
from calendar import monthrange


class GeradorPrevisao:
    @staticmethod
    def obter_previsao_dias_mes():
        # Obter a data atual
        data_atual = datetime.date.today()
        ultimo_dia_mes = data_atual.replace(day=monthrange(data_atual.year, data_atual.month)[1])
        # AJUSTAR PARA ATUALIZACAO NO FINAL DE SEMANA
        PREVISAO = list(range(1, ultimo_dia_mes.day-4))

        return PREVISAO
