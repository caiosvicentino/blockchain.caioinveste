'''Prover metodos de Hash(codificação)'''

import hashlib
import json
from transacoes import Transacoes


def hashing(string):
    return hashlib.sha256(string).hexdigest()


def block_hash(block):
    bloco_hashado = block.__dict__.copy()
    bloco_hashado['transacoes'] = [tx.dict_order() for tx in bloco_hashado['transacoes']]
    return hashing(json.dumps(bloco_hashado, sort_keys=True).encode())
