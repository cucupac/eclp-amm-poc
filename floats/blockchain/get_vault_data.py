import os
import sys

from web3 import Web3
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from abis.vault import ABI as VAULT_ABI
from schemas.vault import VaultTokenInfo
from schemas.token import Token

# For Standarization
from constants import X_0, Y_0

load_dotenv(".env")


def get_initial_token_balances(pool_id: str) -> VaultTokenInfo:
    """Returns the starting balances for both of the tokens in the pool."""
    web3 = Web3(Web3.HTTPProvider(os.environ.get("ETHEREUM_RPC")))

    vault_contract = web3.eth.contract(
        address=os.environ.get("VAULT_ADDRESS"), abi=VAULT_ABI
    )

    pool_tokens = vault_contract.functions.getPoolTokens(pool_id).call()
    # token_0_info = Token(address=pool_tokens[0][0], amount=pool_tokens[1][0])
    # token_1_info = Token(address=pool_tokens[0][1], amount=pool_tokens[1][1])

    token_0_info = Token(address=pool_tokens[0][0], amount=X_0)
    token_1_info = Token(address=pool_tokens[0][1], amount=Y_0)

    return VaultTokenInfo(
        x_0=token_0_info.model_dump(),
        y_0=token_1_info.model_dump(),
    )
