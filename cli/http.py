import json
import requests
from cli.util import Retry, ResponseStatusError

class Client:

    DEFAULT_WAIT_FOR_RESPONSE_TIMEOUT_SECS = 30

    def __init__(self, url, retry=None):
        self._url = url
        self._retry = retry or Retry()
        self._session = requests.Session()

    def eth_get_balance(self, addr, token):
        return self.eth_execute("get_balance", addr=addr, token=token)

    def eth_get_transaction_count(self, addr):
        return self.eth_execute("get_transaction_count", addr=addr)

    def eth_send_tx(self, tx):
        return self.eth_execute("sendtx", tx=tx)

    def eth_estimate_gas(self, tx):
        if isinstance(tx, dict):
            tx = json.dumps(tx)
        return self.eth_execute("estimate_gas", tx=tx)

    def eth_get_gas_price(self):
        return self.eth_execute("get_gas_price")

    def eth_get_chain_id(self):
        return self.eth_execute("get_chain_id")

    def eth_get_contract_info(self, token):
        return self.eth_execute("get_contract_info", token=token)

    def btc_get_utxo(self, addr):
        return self.btc_execute("get_utxo", addr=addr)

    def btc_send_tx(self, tx):
        return self.btc_execute("sendtx", tx=tx)

    def btc_get_balance(self, addr):
        return int(self.btc_execute("get_balance", addr=addr))

    def btc_estimate_fee(self, block_height=1):
        return int(self.btc_execute("estimate_fee", block_height=block_height))

    '''............................called internal...............................'''
    def eth_execute(self, method, **params):
        return self.execute("eth", method, params)

    def btc_execute(self, method, **params):
        return self.execute("btc", method, params)

    def execute(self, chain, method, params):
        return self._retry.execute(
            lambda:self.execute_without_retry(chain, method, params)
        )

    def execute_without_retry(self, chain, method, params):
        params["chain"] = chain
        params["method"] = method
        response = self._session.get(self._url, params=params, timeout=self.DEFAULT_WAIT_FOR_RESPONSE_TIMEOUT_SECS)
        response.raise_for_status()
        response = response.json()
        if response.get("status") == 200:
            return response.get("data")
        raise ResponseStatusError(str(response))

