import os
from violas_client import Client
from violas_client.lbrtypes import NamedChain

'''violas'''
# JSON_RPC_URL: str = "http://ab.testnet.violas.io:50001"
JSON_RPC_URL: str = "http://13.77.137.84:50001"
FAUCET_ADDR = "00000000000000000042524746554e44"
CREATE_ACCOUNT_SERVER="https://api4.violas.io/1.0/violas/mint"


CLIENT_ID = "90f023f9-82b6-4b93-beb6-561743f9af84"
TENANT_ID = "d99eee11-8587-4c34-9201-38d5247df9c9"
SECRET = "eRvgvZxMh_v27EWR5-Z-C2DWo~yc_78jfR"

os.environ["AZURE_CLIENT_ID"] = CLIENT_ID
os.environ["AZURE_TENANT_ID"] = TENANT_ID
os.environ["AZURE_CLIENT_SECRET"] = SECRET

VAULT_NAME = "violas-test-liquidator"
ARBITRAGE_SECRET_NAME = "arbitrage-secret"


'''btc'''

'''eth'''
eth_private_key = "8d14e57809310583f206c425067e4def8e7c11bfd36f958e071bbd1a01f1b043"


'''binance'''
API_KEY = "ORa5qpFXZ0028PkOLCiH8tC6lojJsvT6FoNwuTU7dA3cjhwlR0eRHMy005zWOyGp"
API_SECRET = "xvJ41OUQDGqUJwAROkxA1lnNq1a4rWCLOetNO8mG0msjyp8DajJ7AvFmmfSsojDU"

url = "http://127.0.0.1:10001/"

def create_client():
    return Client.new(JSON_RPC_URL)