from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import Crypto.Random
import binascii



class Wallet:
    def __init__(self):
        self.chave_privada = None
        self.chave_publica = None

    def criar_chave(self):
        chave_privada, chave_publica = self.gerar_keys()
        self.chave_privada = chave_privada
        self.chave_publica = chave_publica


    def salve_chaves(self):
        if self.chave_publica != None and self.chave_privada != None:
            try:
                with open('wallet.txt', mode='w') as f:
                    f.write(self.chave_publica)
                    f.write('\n')
                    f.write(self.chave_privada)
                return True
            except (IOError, IndexError):
                print('Salvar Wallet falhou!')
                return False

    def leia_chaves(self):
        try:
            with open('wallet.txt', mode='r') as f:
                chaves = f.readlines()
                chave_publica = chaves[0][:-1]
                chave_privada = chaves[1]
                self.chave_publica = chave_publica
                self.chave_privada = chave_privada
            return True
        except (IOError, IndexError):
            print('Ler Wallet falhou!')
            return False

    def gerar_keys(self):
        chave_privada = RSA.generate(1024, Crypto.Random.new().read)
        chave_publica = chave_privada.publickey()
        return (binascii.hexlify(chave_privada.exportKey(format='DER')).decode('ascii'), binascii.hexlify(chave_publica.exportKey(format='DER')).decode('ascii'))

    def assinatura_tx(self, pagador, recebedor, valor):
        assinante = PKCS1_v1_5.new(RSA.importKey(binascii.unhexlify(self.chave_privada)))
        h = SHA256.new((str(pagador) + str(recebedor) + str(valor)).encode('utf8'))
        assinatura = assinante.sign(h)
        return binascii.hexlify(assinatura).decode('ascii')

    @staticmethod
    def verificar_tx(transacao):
        chave_publica = RSA.importKey(binascii.unhexlify(transacao.pagador))
        verificar = PKCS1_v1_5.new(chave_publica)
        h = SHA256.new((str(transacao.pagador) + str(transacao.recebedor) + str(transacao.valor)).encode('utf8'))
        return verificar.verify(h, binascii.unhexlify(transacao.assinatura))

