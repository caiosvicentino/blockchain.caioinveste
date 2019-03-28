from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from caiocoin import Blockchain
from wallet import Wallet

app = Flask(__name__)
wallet = Wallet()
blockchain = Blockchain(wallet.chave_publica)
CORS(app)

@app.route('/', methods=['GET'])
def get_ui():
    return send_from_directory('UI', 'node.html')


@app.route('/wallet', methods=['POST'])
def crie_chaves():
    wallet.criar_chave()
    if wallet.salve_chaves():
        global blockchain
        blockchain = Blockchain(wallet.chave_publica)
        resposta = {
            'chave_publica': wallet.chave_publica,
            'chave_privada': wallet.chave_privada,
            'fundos': blockchain.pegue_balanco()
        }
        return jsonify(resposta), 201
    else:
        resposta = {
            'mensagem': 'Salvar as chaves falhou!'
        }
        return jsonify(resposta), 500


@app.route('/wallet', methods=['GET'])
def leia_chaves():
    if wallet.leia_chaves():
        global blockchain
        blockchain = Blockchain(wallet.chave_publica)
        resposta = {
            'chave_publica': wallet.chave_publica,
            'chave_privada': wallet.chave_privada,
            'fundos': blockchain.pegue_balanco()
        }
        return jsonify(resposta), 201
    else:
        resposta = {
            'mensagem': 'Ler as chaves falhou!'
        }
        return jsonify(resposta), 500
    pass


@app.route('/balanco', methods=['GET'])
def pegue_balanco():
    balanco = blockchain.pegue_balanco()
    if balanco != None:
        resposta = {
            'menssagem': 'Balanço realizado com sucesso!',
            'fundos': balanco
        }
        return jsonify(resposta), 200
    else:
        resposta = {
            'menssagem': 'Ler o balanço falhou!',
            'wallet_setup': wallet.chave_publica != None
        }
        return jsonify(resposta), 500


@app.route('/transacao', methods=['POST'])
def add_transacao():
    if wallet.chave_publica == None:
        resposta = {
            'menssagem': 'Configure a sua wallet!'
        }
        return jsonify(resposta), 400
    valores = request.get_json()
    if not valores:
        resposta = {
            'menssagem': 'Sem data disponivel!'
        }
        return jsonify(resposta), 400
    areas_requeridas = ['recebedor', 'valor']
    if not all(areas in valores for areas in areas_requeridas):
        resposta = {
            'menssagem': 'Está faltando data!'
        }
        return jsonify(resposta), 400
    recebedor = valores['recebedor']
    valor = valores['valor']
    assinatura = wallet.assinatura_tx(wallet.chave_publica, recebedor, valor)
    sucesso = blockchain.add_transacao(recebedor, wallet.chave_publica, assinatura, valor)
    if sucesso:
        resposta = {
            'menssagem': 'Transação efetivada com sucesso!',
            'transação': {
                'pagador': wallet.chave_publica,
                'recebedor': recebedor,
                'valor': valor,
                'assinatura': assinatura
            },
            'fundos':blockchain.pegue_balanco()
        }
        return jsonify(resposta), 201
    else:
        resposta = {
            'menssagem': 'Criar uma nova transação falhou!'
        }
        return jsonify(resposta), 500



@app.route('/minere', methods=['POST'])
def mine():
    block = blockchain.minere_blocos()
    if block != None:
        dict_bloco = block.__dict__.copy()
        dict_bloco['transacoes'] = [
            tx.__dict__ for tx in dict_bloco['transacoes']]
        resposta = {
            'mensagem': 'Bloco minerado com sucesso!',
            'bloco': dict_bloco,
            'fundos': blockchain.pegue_balanco()
        }
        return jsonify(resposta), 201
    else:
        resposta = {
            'mensagem': 'Adicionar um bloco falhou!',
            'wallet_setup': wallet.chave_publica != None
        }
        return jsonify(resposta), 500


@app.route('/transacoes', methods=['GET'])
def pegue_transacoes_abertas():
    transacoes = blockchain.pegue_transacao_aberta()
    dict_transacoes = [tx.__dict__ for tx in transacoes]
    return jsonify(dict_transacoes), 200


@app.route('/chain', methods=['GET'])
def pegue_chain():
    foto_chain = blockchain.chain
    dict_chain = [block.__dict__.copy() for block in foto_chain]
    for dict_block in dict_chain:
        dict_block['transacoes'] = [tx.__dict__ for tx in dict_block['transacoes']]
    return jsonify(dict_chain), 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)