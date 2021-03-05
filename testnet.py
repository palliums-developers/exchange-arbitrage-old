import os
from violas_client import Client
from violas_client.lbrtypes import NamedChain


JSON_RPC_URL: str = "http://ab.testnet.violas.io:50001"
CHAIN_ID = NamedChain.TESTING
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



def create_client():
    return Client.new(JSON_RPC_URL, CHAIN_ID)