'''Prover metodos de criação dos nodes'''

from uuid import uuid4

from caiocoin import Blockchain
from utilidade.verificar import Verificar
from wallet import Wallet


class Node:
    def __init__(self, id):
        # self.wallet.chave_publica = str(uuid4())
        self.wallet = Wallet()
        self.wallet.criar_chave()
        self.blockchain = Blockchain(self.wallet.chave_publica)

    def pegue_valor_transacao(self):
        '''Usuario adicona valor como um float. '''
        transacao_recebedor = input('Entre a Chave do Recebedor: ')
        valor_transaçao = float(input('Qual valor da trasação: '))
        return (transacao_recebedor, valor_transaçao)

    def escolha_usuario(self):
        '''Escolha do usuario para as opções do Blockchain'''
        usuario_input = input('Sua escolha: ')
        return usuario_input


    def imprimir_blockchain_elementos(self):
        '''Imprimi os blocos de saida'''
        for block in self.blockchain.chain:
            print('Blocos de Saída.')
            print(block)
        else:
            print('-' * 20)

    def leia_input(self):
        epserando_input = True 
        '''LOOP'''
        while epserando_input:
            '''Loop das Opções do Blockchain / Loop Verificação dos blocos.'''
            print('Por favor, esoclha: ')
            print('1: Add um novo valor para a transação.')
            print('2: Imprimir os blocos do blockchain.')
            print('3: Minere um novo bloco')
            print('4: Verifique a validade das transações')
            print('5: Criar Wallet')
            print('6: Abra Wallet')
            print('7: Salve as Chaves')
            print('8: Sair')
            usuario_escolha = self.escolha_usuario()
            if usuario_escolha == '1':
                tx_data = self.pegue_valor_transacao()
                recebedor, valor = tx_data
                assinatura = self.wallet.assinatura_tx(self.wallet.chave_publica, recebedor, valor)
                if self.blockchain.add_transacao(recebedor,self.wallet.chave_publica, assinatura, valor=valor):
                    print('Transação cocluida com sucesso!')
                else:
                    print('Transação Falhou!')
                print(self.blockchain.pegue_transacao_aberta())
            elif usuario_escolha == '2':
                self.imprimir_blockchain_elementos()
            elif usuario_escolha == '3':
                if not self.blockchain.minere_blocos():
                    print('Mineração falhou, Está sem Wallet?')
            elif usuario_escolha == '4':
                if Verificar.verifique_validade_transacao(self.blockchain.pegue_transacao_aberta(), self.blockchain.pegue_balanco):
                    print('Todas as transações foram validas')
                else:
                    print('Existem transações invalidas')
            elif usuario_escolha == '5':
                self.wallet.criar_chave()
                self.blockchain = Blockchain(self.wallet.chave_publica)
            elif usuario_escolha == '6':
                self.wallet.leia_chaves()
                self.blockchain = Blockchain(self.wallet.chave_publica)
            elif usuario_escolha == '7':
                self.wallet.salve_chaves()
                print('Wallets salvas!')
            elif usuario_escolha == '8':
                epserando_input = False    
            else:
                print('Selecione uma das opções indicadas..')
            if not Verificar.verificar_chain(self.blockchain.chain):
                self.imprimir_blockchain_elementos()
                print('Blockchain foi rompido! Blockchain INVALIDO!')
                break
            print('O saldo de {}, é {:6.2f}'.format(self.wallet.chave_publica, self.blockchain.pegue_balanco()))
            print('-*' * 20)
        else:
            print('Usuario saiu do Blockchain.')

        print('Feito!')

if __name__ == '__main__':
    node = Node(id)
    node.leia_input()
