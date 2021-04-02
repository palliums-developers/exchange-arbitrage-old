from .util import Retry
from binance.client import Client as BClient

class Client:
    def __init__(self, api_key, api_secret, retry=None):
        self._client = BClient(api_key, api_secret)
        self._retry = retry or Retry()

    def get_buy_price(self, currency_code):
        pair_name = self.get_pair_name(currency_code)
        ticker = self.execute(self._client.get_orderbook_ticker, symbol=pair_name)
        return float(ticker.get("bidPrice"))

    def get_sell_price(self, currency_code):
        pair_name = self.get_pair_name(currency_code)
        ticker = self.execute(self._client.get_orderbook_ticker,symbol=pair_name)
        return float(ticker.get("askPrice"))

    def test_buy(self, currency_code, price, amount):
        pair_name = self.get_pair_name(currency_code)
        return self.execute(self._client.create_test_order,
                            symbol=pair_name,
                            side=self._client.SIDE_BUY,
                            type=self._client.ORDER_TYPE_MARKET,
                            price=price,
                            quantity=amount)

    def buy(self, currency_code, price, amount):
        pair_name = self.get_pair_name(currency_code)
        return self.execute(self._client.create_order,
                            symbol=pair_name,
                            side=self._client.SIDE_BUY,
                            type=self._client.ORDER_TYPE_MARKET,
                            price=price,
                            quantity=amount)

    def test_sell(self, currency_code, amount):
        pair_name = self.get_pair_name(currency_code)
        return self.execute(self._client.create_test_order,
                            symbol=pair_name,
                            side=self._client.SIDE_SELL,
                            type=self._client.ORDER_TYPE_MARKET,
                            quantity=amount)

    def sell(self, currency_code, amount):
        pair_name = self.get_pair_name(currency_code)
        return self.execute(self._client.create_order,
                            symbol=pair_name,
                            side=self._client.SIDE_SELL,
                            type=self._client.ORDER_TYPE_MARKET,
                            quantity=amount)

    def get_buy_trade_fee(self, currency_code):
        pair_name = self.get_pair_name(currency_code)
        info = self.execute(self._client.get_trade_fee, symbol=pair_name)
        return info["tradeFee"][0]["taker"]

    def get_sell_trade_fee(self, currency_code):
        pair_name = self.get_pair_name(currency_code)
        info = self.execute(self._client.get_trade_fee, symbol=pair_name)
        return info["tradeFee"][0]["maker"]

    def get_buy_value(self, currency_code, amount):
        '''
        购买指定数量的currency，需要多少usdt
        '''
        pair_name = self.get_pair_name(currency_code)
        ticker = self.execute(self._client.get_orderbook_ticker,symbol=pair_name)
        price = float(ticker.get("bidPrice"))
        info = self.execute(self._client.get_trade_fee, symbol=pair_name)
        fee = info["tradeFee"][0]["taker"]
        return amount * price / (1-fee)

    def get_sell_value(self, currency_code, amount):
        '''
        卖出指定数量的currency，可以获取多少usdt
        '''
        pair_name = self.get_pair_name(currency_code)
        ticker = self.execute(self._client.get_orderbook_ticker, symbol=pair_name)
        price = float(ticker.get("askPrice"))
        info = self.execute(self._client.get_trade_fee, symbol=pair_name)
        fee = info["tradeFee"][0]["maker"]
        return amount * price * (1-fee)

    @staticmethod
    def get_pair_name(currency_code):
        return currency_code + "USDT"

    def execute(self, fn, **kwargs):
        return self._retry.execute(
            lambda :fn(**kwargs)
        )


