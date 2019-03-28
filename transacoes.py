'''Prover metodos de transações'''


from collections import OrderedDict
from utilidade.imprimir import Imprimir


class Transacoes(Imprimir):
    def __init__(self, pagador, recebedor, assinatura, valor):
        self.pagador = pagador
        self.recebedor = recebedor
        self.valor = valor
        self.assinatura = assinatura
    
    def dict_order(self):
        return OrderedDict([('pagador', self.pagador), ('recebedor', self.recebedor), ('valor', self.valor)])

