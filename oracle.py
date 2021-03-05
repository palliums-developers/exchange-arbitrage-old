import violas_client


def get_currency_price(client: violas_client.Client, currency_code):
    ex_rate = client.oracle_get_exchange_rate(currency_code)
    if ex_rate is not None:
        return ex_rate.value / 2**32

if __name__ == "__main__":
    from testnet import create_client
    client = create_client()
    price = get_currency_price(client, "vBTC")
    print(price)