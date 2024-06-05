import os
import sys
from typing import Tuple

from web3 import Web3
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from abis.eclp_gyd_sdai import ABI as POOL_ABI
from integers.schemas.pool import Params, DerivedParams, R
from constants import INVARIANT_X, INVARIANT_Y

load_dotenv(".env")


def __get_pool_contract() -> Web3:
    web3 = Web3(Web3.HTTPProvider(os.environ.get("ETHEREUM_RPC")))

    return web3.eth.contract(address=os.environ.get("POOL_ADDRESS"), abi=POOL_ABI)


def __get_swap_fee_percentage() -> int:
    """Returns the current swap fee percentage for the pool."""

    pool_contract = __get_pool_contract()
    return pool_contract.functions.getSwapFeePercentage().call()


def get_effective_amount_in_percentage() -> float:
    swap_fee_percentage = __get_swap_fee_percentage() / 1e18
    return 1 - swap_fee_percentage


def get_pool_id() -> str:
    """Returns the pool id for the pool."""

    pool_contract = __get_pool_contract()
    return "0x" + pool_contract.functions.getPoolId().call().hex()


def get_invariant() -> R:
    """
    Returns the current invariant for the pool. This function
    does not take invariant error into account.
    """

    # pool_contract = __get_pool_contract()
    # invariant = pool_contract.functions.getInvariant().call()

    """HARD CODE INITIAL INVARIANT TO MATCH INITIAL BALANCES."""
    return R(x=INVARIANT_X, y=INVARIANT_Y)


def get_eclp_parmas() -> Tuple[Params, DerivedParams]:
    """Returns the ECLP parameters for the pool."""

    pool_contract = __get_pool_contract()

    eclp_parmas_params = pool_contract.functions.getECLPParams().call()

    params = Params(
        alpha=eclp_parmas_params[0][0],
        beta=eclp_parmas_params[0][1],
        c=eclp_parmas_params[0][2],
        s=eclp_parmas_params[0][3],
        λ=eclp_parmas_params[0][4],
    )

    d = DerivedParams(
        tau_alpha_x=eclp_parmas_params[1][0][0],
        tau_alpha_y=eclp_parmas_params[1][0][1],
        tau_beta_x=eclp_parmas_params[1][1][0],
        tau_beta_y=eclp_parmas_params[1][1][1],
        u=eclp_parmas_params[1][2],
        v=eclp_parmas_params[1][3],
        w=eclp_parmas_params[1][4],
        z=eclp_parmas_params[1][5],
        d_sq=eclp_parmas_params[1][6],
    )

    print("\n\n")
    for key, value in params.model_dump().items():
        print(key, value)

    for key, value in d.model_dump().items():
        print(key, value)

    return params, d
