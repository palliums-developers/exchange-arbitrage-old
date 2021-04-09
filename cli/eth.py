from web3 import Web3
from network import eth_url_prefix, contracts, e2v_token

class Client:

    WAIT_TRANSATION_TIMEOUT = 120

    def __init__(self):
        self._w3 = Web3(Web3.HTTPProvider(eth_url_prefix))
        self._contracts = contracts
        self._e2v_addr, self._e2v_abi = self._get_contract_info(e2v_token)

    def get_balance(self, addr, token):
        token = token.lower()
        if token == "eth":
            return self._w3.eth.get_balance(addr)
        token_addr, abi = self._get_contract_info(token)
        contract = self._w3.eth.contract(token_addr, abi=abi)
        return contract.functions.balanceOf(addr).call()

    def transfer(self, priv_key, to_addr, token, amount):
        token = self._to_standard(token)
        ac = self._w3.eth.account.from_key(priv_key)
        if token == "eth":
            tx = self._create_eth_tx(ac, to_addr, amount)
        else:
            tx = self._create_contract_tx(ac, token, "transfer", to_addr, amount)
        tx_hash = self._w3.eth.send_raw_transaction(tx)
        self._w3.eth.waitForTransactionReceipt(tx_hash, self.WAIT_TRANSATION_TIMEOUT)
        return tx_hash

    def to_violas(self, priv_key, violas_addr, token, amount):
        token = self._to_standard(token)
        ac = self._w3.eth.account.from_key(priv_key)
        token_addr, _ = self._get_contract_info(token)
        allownce = self.call_method(token, "allowance", ac.address, self._e2v_addr)
        if allownce != 0:
            self.exec_method(priv_key, token, "approve", self._e2v_addr, 0)

        self.exec_method(priv_key, token, "approve", self._e2v_addr, amount)
        return self.exec_method(priv_key, e2v_token, "transferProof", token_addr, violas_addr)

    def exec_method(self, priv_key, token, method, *args):
        token = self._to_standard(token)
        ac = self._w3.eth.account.from_key(priv_key)
        tx = self._create_contract_tx(ac, token, method, *args)
        tx_hash = self._w3.eth.send_raw_transaction(tx)
        self._w3.eth.waitForTransactionReceipt(tx_hash, self.WAIT_TRANSATION_TIMEOUT)
        return tx_hash

    def call_method(self, token, method, *args):
        token = self._to_standard(token)
        token_addr, abi = self._get_contract_info(token)
        contract = self._w3.eth.contract(token_addr, abi=abi)
        return getattr(contract.functions, method)(*args).call()

    def _create_eth_tx(self, ac, to_addr, amount):
        raw_tx = dict(
            nonce=self._w3.eth.get_transaction_count(ac.address),
            to=to_addr,
            value=amount,
            data="",
            gasPrice=self._w3.eth.gas_price or self._w3.eth.gasPrice(),
            chainId=self._w3.eth.chain_id or self._w3.eth.chainId(),
        )
        raw_tx["gas"] = self._w3.eth.estimateGas(raw_tx)
        signed_tx = ac.signTransaction(raw_tx)
        return signed_tx.rawTransaction.hex()

    def _create_contract_tx(self, ac, token, method, *args):
        contract_addr, abi = self._get_contract_info(token)
        contract = self._w3.eth.contract(contract_addr, abi=abi)
        data = getattr(contract.functions, method)(*args)

        raw_tx = data.buildTransaction({
            "nonce": self._w3.eth.get_transaction_count(ac.address),
            "gasPrice": self._w3.eth.gas_price or self._w3.eth.gasPrice(),
            "chainId": self._w3.eth.chain_id or self._w3.eth.chainId(),
            "gas": data.estimateGas({"from": ac.address}),
        })
        signed_tx = ac.signTransaction(raw_tx)
        return signed_tx.rawTransaction.hex()

    def _get_contract_info(self, token):
        info = self._contracts.get(token)
        if info is None:
            info = self._w3.eth.contract(token)
        return info

    def _to_standard(self, token):
        return token.lower()







