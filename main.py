from network import *
from cli.eth import Client
from eth_account import Account

to_addr = "0x4d6Bb4ed029B33cF25D0810b029bd8B1A6bcAb7B"

cli = Client(url)
sender = Account.from_key(eth_private_key)
cli.transfer(sender, to_addr, "vlstusdt", 234325)

