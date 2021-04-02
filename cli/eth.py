import json
from web3 import Web3
from eth_account.signers.local import LocalAccount

from .http import Client as HClient

project_id = "63f370f2e4dc41c5bd6a6f2234435300"
project_secret = "33d95e9759734ba6b0a296c6af50d104"
eth_url_prefix = f"https://kovan.infura.io/v3/{project_id}"

class Client(HClient):

    def __init__(self, url, retry=None):
        super().__init__(url, retry)
        # self._w3 = Web3(Web3.HTTPProvider(eth_url_prefix))
        self._w3 = Web3()

    def transfer(self, from_account: LocalAccount, to_addr, token, amount):
        token = token.lower()
        if token == "eth":
            return self.eth_send_tx(self.create_eth_tx(from_account, to_addr, amount))
        return self.eth_send_tx(self.create_erc20_tx(from_account, to_addr, token, amount))

    def create_eth_tx(self, from_account: LocalAccount, to_address, amount):
        raw_tx = dict(
            nonce=self.eth_get_transaction_count(from_account.address),
            to=to_address,
            value=amount,
            data="",
            gasPrice=self.eth_get_gas_price(),
            chainId=self.eth_get_chain_id(),
        )
        raw_tx["gas"] = self.eth_estimate_gas(json.dumps(raw_tx))
        signed_tx = from_account.signTransaction(raw_tx)
        return signed_tx.rawTransaction.hex()

    def create_erc20_tx(self, from_account: LocalAccount, to_addr, token, amount):
        contract_addr, abi = self.eth_get_contract_info(token)
        contract_addr = self._w3.toChecksumAddress(contract_addr)
        contract = self._w3.eth.contract(contract_addr, abi=abi)
        data = contract.functions.transfer(to_addr, amount)
        raw_tx = data.buildTransaction(dict(
            nonce=self.eth_get_transaction_count(from_account.address),
            gasPrice=self.eth_get_gas_price(),
            chainId=self.eth_get_chain_id(),
            gas = 1,
        ))
        raw_tx["from"] = from_account.address
        raw_tx["gas"] = self.eth_estimate_gas(raw_tx)
        signed_tx = from_account.signTransaction(raw_tx)
        return signed_tx.rawTransaction.hex()

