import typing
import requests
from cryptos import Bitcoin
from cryptos.main import privkey_to_pubkey, privkey_to_address

from cli.util import AmountNotEnough, gen_b2v_data
from network import *
from cli.util import Retry
from network import magicbyte, testnet

class InvalidMethodError(Exception):
    pass

class Account:
    def __init__(self, private_key):
        self.private_key = private_key
        self.public_key = privkey_to_pubkey(private_key)
        self.address = privkey_to_address(self.private_key, magicbyte)

class Client:

    DEFAULT_CONNECT_TIMEOUT_SECS: float = 5.0
    DEFAULT_TIMEOUT_SECS: float = 30.0

    def __init__(self, retry=None):
        self._retry = retry or Retry()
        self._session = requests.session()
        self._method_to_urls = btc_method_to_urls
        self._btc = Bitcoin(testnet=testnet)
        self._timeout = (self.DEFAULT_CONNECT_TIMEOUT_SECS, self.DEFAULT_TIMEOUT_SECS)

    def transfer(self, from_account: Account, to_address, amount):
        utxos = self.get_utxo(from_account.address)
        sum, inputs = self.get_inputs(amount, utxos)
        fee = self.estimate_fee(1)
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
        return self.send_transction(signed_tx)

    def to_violas(self, from_account, amount, violas_addr, chain_id):
        fee = self.estimate_fee()
        utxos = self.get_utxo(from_account.address)
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
        return self.send_transction(signed_tx)

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


    def get_transaction(self, txid):
        return self._retry.execute(
            lambda:self.execute("tx", [txid])
        )

    def get_account_info(self, addr):
        return self._retry.execute(
            self.execute("address", [addr])
        )

    def get_balance(self, addr):
        return self._retry.execute(
            lambda :self.get_account_info(addr).get("balance")
        )

    def get_utxo(self, addr):
        return self._retry.execute(
            lambda :self.execute("utxo", [addr])
        )

    def send_transction(self, tx):
        return self._retry.execute(
            lambda :self.execute("sendtx", [tx])
        )

    def estimate_fee(self, block_height=1):
        fee = self._retry.execute(
            lambda :self.execute("estimatefee", [block_height]).get("result")
        )
        return int(float(fee)*10**8)


    def execute(self, method, params):
        url = self._method_to_urls.get(method)
        if url is None:
            raise InvalidMethodError(f"{method} is not valid method")
        for param in params:
            url += str(param)
        return self.get(url)

    def get(self, url):
        response = self._session.get(url, timeout=self._timeout)
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    cli = Client()
    ac = Account(btc_private_key)
    cli.to_violas(ac, 300000, "b14bc3286e4b9b41c86022f2e614d721", chain_id=2)