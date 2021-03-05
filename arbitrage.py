from violas_client import Client
from sympy import *
from sympy.abc import x, y

from oracle import get_currency_price
from account import get_arbitrage_account
from faucet import try_apply_coin
from http_client import Client as HttpClient
from network import CREATE_ACCOUNT_SERVER


MIN_ARBITRAGE_VALUE = 10_000
arbitrage_account = get_arbitrage_account()
http_client = HttpClient(CREATE_ACCOUNT_SERVER)

def get_arbitrage_amount_in(reserve_in, reserve_out, price_in, price_out):
    results = solve([y-x*reserve_out/(reserve_in+x), (reserve_out-y)/(reserve_in+x)-price_in/price_out])
    for result in results:
        amount_in = result.get(x)
        amount_out = result.get(y)
        if amount_in > 0 and amount_out > 0:
            return amount_in

def get_amount_out(amount_in, reserve_in, reserve_out):
        return Client.get_output_amount(amount_in, reserve_in, reserve_out)

def get_arbitrage_amount(reserve_in, reserve_out, price_in, price_out):
    amount_in = get_arbitrage_amount_in(reserve_in, reserve_out, price_in, price_out)
    if amount_in is not None:
        amount_out = get_amount_out(amount_in, reserve_in, reserve_out)
        if amount_out * price_out - amount_in * price_in > MIN_ARBITRAGE_VALUE:
            return int(amount_in), int(amount_out)

def check_pair(client: Client, currency_a, currency_b):
    price_a = get_currency_price(client, currency_a)
    price_b = get_currency_price(client, currency_b)
    index_a, index_b = client.swap_get_currency_indexs(currency_a, currency_b)
    reserves = client.swap_get_reserves_resource()
    reserve = client.get_reserve(reserves, index_a, index_b)
    reserve_a, reserve_b = reserve.coina.value, reserve.coinb.value
    #套利a换b
    if reserve_a * price_a < reserve_b * price_b:
        result = get_arbitrage_amount(reserve_a, reserve_b, price_a, price_b)
        if result is not None:
            return result[0], None
    else:
        result = get_arbitrage_amount(reserve_b, reserve_a, price_b, price_a)
        if result is not None:
            return None, result[0]
    return None, None

def do_arbitrage(client: Client, currency_in, currency_out, amount_in):
    balance = client.get_balance(arbitrage_account.address_hex, currency_in)
    if balance is None or balance < amount_in:
        try_apply_coin(client, arbitrage_account, currency_in, amount_in, http_client)
        return
    if currency_out not in client.get_account_registered_currencies(arbitrage_account.address_hex):
        client.add_currency_to_account(arbitrage_account, currency_out)
    client.swap(arbitrage_account, currency_in, currency_out, amount_in)

def exchange_arbitrage(client: Client):
    reserves = client.swap_get_reserves_resource()
    pairs = client.get_pairs(reserves)
    for index_a, index_b in pairs:
        currency_a, currency_b = client.swap_get_currency_codes(index_a, index_b)
        a_in_amount, b_in_amount = check_pair(client, currency_a, currency_b)
        if a_in_amount is not None:
            do_arbitrage(client, currency_a, currency_b, a_in_amount)
        elif b_in_amount is not None:
            do_arbitrage(client, currency_b, currency_a, b_in_amount)
