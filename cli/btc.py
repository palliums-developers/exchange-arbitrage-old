from cryptos import Bitcoin
from cryptos.main import privkey_to_pubkey, pubkey_to_address

from .util import AmountNotEnough
from .http import Client as HClient

class Account:
    def __init__(self, private_key):
        self.private_key = private_key
        self.public_key = privkey_to_pubkey(private_key)
        self.address = pubkey_to_address(self.public_key)

class Client(HClient):
    def __init__(self, url, retry=None):
        super().__init__(url, retry)
        self._btc = Bitcoin()

    def transfer(self, from_account: Account, to_address, amount, token):
        utxos = self.btc_get_utxo(from_account.address)
        inputs = self.get_inputs(amount, utxos)
        outs = [{
            "output": f"{to_address}:0",
            "value": amount
        }]
        tx = self.create_tx(inputs, outs)
        signed_tx = self._btc.signall(tx, from_account.private_key)
        return self.btc_send_tx(signed_tx)

    def create_tx(self, inputs, outs):
        return self._btc.mktx(inputs, outs)

    def get_inputs(self, amount, utxos):
        sum = 0
        ret = []
        for utxo in utxos:
            sum += utxo.get("value")
            ret.append(utxo)
            if sum >= amount:
                return ret
        raise AmountNotEnough(f"Account not has {amount} btc")
