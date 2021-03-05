from violas_client import Client
from account import get_arbitrage_account

client = Client("violas_testnet")
ac = get_arbitrage_account()
# print(client.get_balances(ac.address_hex))
btc_balance = client.get_balance(ac.address_hex, "vBTC")
client.swap(ac, "vBTC", "vUSDT", btc_balance)
