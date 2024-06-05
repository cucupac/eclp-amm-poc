import os
import sys

from web3 import Web3
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from abis.erc20 import ABI as ERC20_ABI
from schemas.vault import VaultTokenInfo

load_dotenv(".env")


def get_token_decimals(vault_token_info: VaultTokenInfo) -> VaultTokenInfo:
    """Get the decimals of a token."""
    web3 = Web3(Web3.HTTPProvider(os.environ.get("ETHEREUM_RPC")))

    for token_name in ["x_0", "y_0"]:
        token = getattr(vault_token_info, token_name)
        address = token.address

        token_contract = web3.eth.contract(address=address, abi=ERC20_ABI)

        decimals = token_contract.functions.decimals().call()

        token.decimals = decimals

    return vault_token_info
