from violas_client import Client, Wallet
from account import get_arbitrage_account

client = Client("violas_testnet")
wallet = Wallet.new()
a1 = wallet.new_account()
client.mint_coin(a1.address_hex, 100_000_000_000, auth_key_prefix=a1.auth_key_prefix, currency_code="vBTC")
client.add_currency_to_account(a1, "vUSDT")
client.swap(a1, "vBTC", "vUSDT", 1_000_000_00)


