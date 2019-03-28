'''Prover metodos de verificação'''

from utilidade.hash_util import hashing, block_hash
from wallet import Wallet


class Verificar:
    @staticmethod
    def prova_valida(transacoes, ultimo_hash, prova):
        guess = (str([tx.dict_order() for tx in transacoes]) + str(ultimo_hash) + str(prova)).encode()
        # print(guess) debug
        pow_hash = hashing(guess)
        # print(pow_hash) debug
        return pow_hash[0:2] == '00'

    @classmethod
    def verificar_chain(cls, blockchain):
        '''Verificador de chain para validar os blocos e retornar True ou False'''
        for (index, bloco) in enumerate(blockchain):
            if index == 0:
                continue
            if bloco.hash_antiga != block_hash(blockchain[index -1]):
                return False
            if not cls.prova_valida(bloco.transacoes[:-1], bloco.hash_antiga, bloco.prova):
                print('Prova de trabalho invalida!')
                return False
            return True

    @staticmethod 
    def verifique_transacao(transacao,pegue_balanco, confira_fundos=True):
        if confira_fundos:
            balanco_pagador = pegue_balanco()
            return balanco_pagador >= transacao.valor and Wallet.verificar_tx(transacao)
        else:
            return Wallet.verificar_tx(transacao)

    @classmethod
    def verifique_validade_transacao(cls,transacoes_abertas, pegue_balanco):
        return all([cls.verifique_transacao(tx, pegue_balanco, False) for tx in transacoes_abertas])
    
   