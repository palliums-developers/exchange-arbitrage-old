import os
import time
import json
import violas_client
from http_client import Client
from network import FAUCET_ADDR
from oracle import get_currency_price


last_apply_times = {}
APPLY_INTERVAL = 60*60*60

MAX_OWN_VALUE = 10_000_000_000
KEEP_VALUE = 1_000_000_000

def get_apply_time(currency_code):
    pair = last_apply_times.get(currency_code)
    if pair is None:
        return 0
    return pair[1]

def get_apply_amount(currency_code):
    pair = last_apply_times.get(currency_code)
    if pair is None:
        return 0
    return pair[0]

def set_apply_time(currency_code, t, amount):
    last_apply_times[currency_code] = (amount,t)

def reset_apply_time(currency_code):
    last_apply_times[currency_code] = (0, 0)

def check(currency_code, amount):
    last_apply_time = get_apply_time(currency_code)
    last_apply_amount = get_apply_amount(currency_code)
    cur_time = time.time()
    if last_apply_time == 0:
        return True
    if cur_time - last_apply_time > APPLY_INTERVAL:
        return True
    if last_apply_amount < amount:
        return True


def try_apply_coin(client: violas_client.Client, ac, currency_code, amount, http_client: Client):

    print("try apply coin")
    if client.get_account_state(ac.address) is None:
        http_client.try_create_child_vasp_account(ac)
    if check(currency_code, amount) and client.get_balance(FAUCET_ADDR, currency_code) > amount:
        set_apply_time(currency_code, time.time(), amount)
        tran_id = f"{os.urandom(16).hex()}"
        # 添加币种支持
        if currency_code not in client.get_account_registered_currencies(ac.address):
            client.add_currency_to_account(ac, currency_code)

        data = {
            "flag":"violas",
            "type":"funds",
            "opttype":"swap",
            "chain": "violas",
            "tran_id": tran_id,
            "token_id": currency_code,
            "amount": amount,
            "to_address": f"0x{ac.address_hex}",
            "state":"start",
            "chain_id": int(client.chain_id)
        }
        client.transfer_coin(ac, FAUCET_ADDR, 1, data=json.dumps(data))
        print("do apply coin", currency_code, amount)

def try_back_coin(client: violas_client.Client, ac, currency_code):
    print("try_back_coin")
    out_price = get_currency_price(client, currency_code)
    out_amount = client.get_balance(ac.address_hex, currency_code)
    if out_amount * out_price > MAX_OWN_VALUE:
        amount = int((out_price * out_amount - KEEP_VALUE) / out_price)
        client.transfer_coin(ac, FAUCET_ADDR, amount, currency_code=currency_code)
        print("do back coin", currency_code, amount)

if __name__ == "__main__":
    data ={'flag': 'violas', 'type': 'funds', 'opttype': 'map', 'chain': 'violas', 'tran_id': 'f9a823872cd872ab31f1d5181fbb0125', 'token_id': 'vUSDT', 'amount': 286519965862.158, 'to_address': '0x716abbc60eb9158cf1909ad23fae8475', 'state': 'start', 'chain_id': 4}

    print(json.dumps(data))