'''Prover metodos de criação do bloco'''

from time import time
from utilidade.imprimir import Imprimir


class Bloco(Imprimir):
    def __init__(self, index, hash_antiga, transacoes, prova, timestamp=time()):
        self.index = index
        self.hash_antiga = hash_antiga
        self.timestamp = timestamp if time is None else timestamp
        self.transacoes = transacoes
        self.prova = prova

