import os
import sys

from web3 import Web3
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from abis.vault import ABI as VAULT_ABI
from integers.schemas.vault import TokenBalances
from constants import X_0, Y_0

load_dotenv(".env")


def get_initial_token_balances(pool_id: str) -> TokenBalances:
    """Returns the starting balances for both of the tokens in the pool."""
    web3 = Web3(Web3.HTTPProvider(os.environ.get("ETHEREUM_RPC")))

    vault_contract = web3.eth.contract(
        address=os.environ.get("VAULT_ADDRESS"), abi=VAULT_ABI
    )

    # pool_tokens = vault_contract.functions.getPoolTokens(pool_id).call()

    """HARD CODE INITIAL BALANCES TO MATCH INVARIANT."""
    return TokenBalances(x_0=X_0, y_0=Y_0)
