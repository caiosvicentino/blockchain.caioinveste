# blockchain.caioinveste '''caiocoin'''


'''Importando pacotes CORE'''
from functools import reduce
import hashlib 
import json
import pickle
from collections import OrderedDict


'''Importando pacotes dos arquivos'''
from utilidade.hash_util import  block_hash
from bloco import Bloco
from transacoes import Transacoes
from utilidade.verificar import Verificar
from wallet import Wallet

reconpensa_mineracao = 10

print(__name__)

'''Iniciando blockchain (vazio)'''
class Blockchain:
    def __init__(self, id_node):
        genesis_bloco = Bloco(0, '', [], 100, 0)
        self.chain = [genesis_bloco]
        self.__transacoes_abertas = []
        self.leia_data()
        self.id_node = id_node

    @property
    def chain(self):
        return self.__chain[:]

    @chain.setter
    def chain(self, val):
        self.__chain = val

    def pegue_transacao_aberta(self):
        return self.__transacoes_abertas[:]


    def leia_data(self):
        try:
            with open('blockchain.txt', mode='r') as leia:
                '''PICKLE'''
                # conteudo_arquivo = pickle.loads(leia.read()) 
                '''JSON'''
                conteudo_arquivo = leia.readlines()
                # blockchain = conteudo_arquivo['chain']
                # transacoes_abertas = conteudo_arquivo['transacao_aberta']
                
                blockchain = json.loads(conteudo_arquivo[0][:-1])
                blockchain_atualizado = []
                for block in blockchain:
                    tx_conversao = [Transacoes(tx['pagador'], tx['recebedor'], tx['assinatura'], tx['valor']) for tx in block['transacoes']]
                    bloco_atualizado = Bloco(block['index'], block['hash_antiga'], tx_conversao, block['prova'], block['timestamp']) 
                    blockchain_atualizado.append(bloco_atualizado)
                self.chain = blockchain_atualizado
                transacoes_abertas = json.loads(conteudo_arquivo[1])
                transacoes_atualizadas = []
                for tx in transacoes_abertas:
                    transacoes_atualizada = Transacoes(tx['pagador'], tx['recebedor'],tx['assinatura'], tx['valor'])
                    transacoes_atualizadas.append(transacoes_atualizada)
                self.__transacoes_abertas = transacoes_atualizadas
        except (IOError, IndexError):
                print('Exceção concedida!')
                pass
        finally:
            print('Tudo certo.')


    def salve_data(self):
        try:
            with open('blockchain.txt', mode='w') as arquivo:
                '''JSON'''
                chain_salvavel = [bloco.__dict__ for bloco in [Bloco(bloco_el.index, bloco_el.hash_antiga, [tx.__dict__ for tx in bloco_el.transacoes] ,bloco_el.prova, bloco_el.timestamp) for bloco_el in self.__chain]]
                arquivo.write(json.dumps(chain_salvavel))
                arquivo.write('\n')
                tx_salvavel = [tx.__dict__ for tx in self.__transacoes_abertas]
                arquivo.write(json.dumps(tx_salvavel))
                '''PICKLE'''
                # salve_data = {
                #     'chain': blockchain,
                #     'transacao_aberta': transacoes_abertas
                # }
                # arquivo.write(pickle.dumps(salve_data))
        except IOError:
            print('Salvar falhou..')


    def prova_de_trabalho(self):
        ultimo_bloco = self.__chain[-1]
        ultimo_hash = block_hash(ultimo_bloco)
        prova = 0
        while not Verificar.prova_valida(self.__transacoes_abertas, ultimo_hash, prova):
            prova += 1
        return prova



    def pegue_balanco(self):
        if self.id_node == None:
            return None
        participante = self.id_node
        tx_pagador = [ [tx.valor for tx in block.transacoes
                    if tx.pagador == participante] for block in self.__chain]
        transacao_aberta_pagador = [tx.valor
                    for tx in self.__transacoes_abertas if tx.pagador == participante]
        tx_pagador.append(transacao_aberta_pagador)
        print(tx_pagador)
        valor_enviado = reduce(lambda tx_soma, tx_valor: tx_soma + sum(tx_valor)
                    if len(tx_valor) > 0 else tx_soma + 0, tx_pagador, 0)
        tx_recebedor = [ [tx.valor
                    for tx in block.transacoes if tx.recebedor == participante] for block in self.__chain]
        valor_recebido = reduce(lambda tx_soma, tx_valor: tx_soma + sum(tx_valor)
                    if len(tx_valor) > 0 else tx_soma + 0, tx_recebedor, 0)
        return valor_recebido - valor_enviado


    def pegue_ultimo_valor_blockchain(self):
        '''Ultimo valor adicionado ao blockchain.'''
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]


    def add_transacao(self, recebedor, pagador, assinatura, valor=1.0):
        '''Add valor ao blockchain.'''
        # transacao = {
        #     'pagador': pagador,
        #     'recebedor': recebedor,
        #     'valor': valor
        # }
        if self.id_node == None:
            return False
        transacao = Transacoes(pagador, recebedor,assinatura, valor)
        if Verificar.verifique_transacao(transacao, self.pegue_balanco):
            self.__transacoes_abertas.append(transacao)
            self.salve_data()
            return True
        return False



    def minere_blocos(self):
        if self.id_node == None:
            return None
        ultimo_bloco = self.__chain[-1]
        hashed_bloco = block_hash(ultimo_bloco)
        prova = self.prova_de_trabalho()
        # reconpensa_transacao = {
        #     'pagador': 'Mineracao',
        #     'recebedor': dono,
        #     'valor': reconpensa_mineracao
        # }
        reconpensa_transacao = Transacoes('Mineracao', self.id_node, '', reconpensa_mineracao)
        transacao_copiadas = self.__transacoes_abertas[:]
        for tx in transacao_copiadas:
            if not Wallet.verificar_tx(tx):
                return None
        transacao_copiadas.append(reconpensa_transacao)
        bloco = Bloco(len(self.__chain), hashed_bloco, transacao_copiadas, prova)
        self.__chain.append(bloco)
        self.__transacoes_abertas = []
        self.salve_data()
        return bloco

