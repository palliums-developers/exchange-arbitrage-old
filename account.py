import azure
from violas_client import Wallet
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from network import VAULT_NAME, ARBITRAGE_SECRET_NAME

def get_arbitrage_account():
    credential = DefaultAzureCredential()
    secret_client = SecretClient(vault_url=f"https://{VAULT_NAME}.vault.azure.net/", credential=credential)
    try:
        secret = secret_client.get_secret(ARBITRAGE_SECRET_NAME).value
    except azure.core.exceptions.ResourceNotFoundError:
        wallet = Wallet.new()
        wallet.new_account()
        secret = wallet.mnemonic
        secret_client.set_secret(ARBITRAGE_SECRET_NAME, secret)
    wallet = Wallet.new_from_mnemonic(secret)
    return wallet.new_account()


if __name__ == "__main__":
    ac = get_arbitrage_account()
    print(ac.address_hex)