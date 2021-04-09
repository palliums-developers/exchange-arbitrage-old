import web3
from web3 import Web3
from network import *


# def test_eth():
#     from cli.eth import Client
#     from testnet import e2v_contract_addr, eth_private_key
#     cli = Client()
#     addr = "0xC95A0C814B2111913416B6B6d29A898c0e513E61"
#     to_addr = e2v_contract_addr
#     print(cli.get_balance(addr, "vlstusdt"))
#     cli.transfer(eth_private_key, to_addr, "vlstusdt", 88)
#
# def test_map():
#     from cli.eth import Client
#     cli = Client()
#     from web3 import Web3
#     from testnet import e2v_contract_addr, eth_private_key
#     addr = "0xC95A0C814B2111913416B6B6d29A898c0e513E61"
#     violas_addr = "b14bc3286e4b9b41c86022f2e614d721"
#     cli.to_violas(eth_private_key, violas_addr, "vlstusdt", 3*10**7)
#
# test_map()