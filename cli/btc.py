from cryptos import Bitcoin
from cryptos.main import privkey_to_pubkey, privkey_to_address

from cli.util import AmountNotEnough, gen_b2v_data
from cli.http import Client as HClient
from network import btc_map_addr

testnet=True
magicbyte=111

class Account:
    def __init__(self, private_key):
        self.private_key = private_key
        self.public_key = privkey_to_pubkey(private_key)
        self.address = privkey_to_address(self.private_key, magicbyte)

class Client(HClient):
    def __init__(self, url, retry=None):
        super().__init__(url, retry)
        self._btc = Bitcoin(testnet=testnet)

    def transfer(self, from_account: Account, to_address, amount):
        utxos = self.btc_get_utxo(from_account.address)
        sum, inputs = self.get_inputs(amount, utxos)
        fee = self.btc_estimate_fee()
        outs = [{
            "address": to_address,
            "value": amount
        },{
            "address": from_account.address,
            "value": sum - amount - fee
        }
        ]

        tx = self.create_tx(inputs, outs)
        signed_tx = self._btc.signall(tx, from_account.private_key)
        return self.btc_send_tx(signed_tx)

    def map_to_violas(self, from_account, amount, violas_addr, chain_id):
        fee = self.btc_estimate_fee()
        utxos = self.btc_get_utxo(from_account.address)
        sum, inputs = self.get_inputs(amount+fee, utxos)
        outs = [{
            "address": btc_map_addr,
            "value": amount
        },{
            "address": from_account.address,
            "value": sum - amount - fee
        },{
            "script": gen_b2v_data(violas_addr, chain_id),
            "value": 0
        }
        ]
        tx = self.create_tx(inputs, outs)
        signed_tx = self._btc.signall(tx, from_account.private_key)
        return self.btc_send_tx(signed_tx)

    def create_tx(self, inputs, outs):
        return self._btc.mktx(inputs, outs)

    def get_inputs(self, amount, utxos):
        sum = 0
        ret = []
        for utxo in utxos:
            sum += int(utxo.get("value"))
            ret.append({
                "output": f"{utxo.get('txid')}:{utxo.get('vout')}",
                'value':int(utxo.get('value'))
            })
            if sum >= amount:
                return sum, ret
        raise AmountNotEnough(f"Account not has {amount} btc")

