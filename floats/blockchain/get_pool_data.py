import os
import sys
from typing import Tuple

from web3 import Web3
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from abis.eclp_gyd_sdai import ABI as POOL_ABI
from schemas.pool import Params, DerivedParams, RateProviders

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


def get_rate_providers() -> RateProviders:
    """Returns the rate provider addresses."""

    pool_contract = __get_pool_contract()

    rate_provider_0 = pool_contract.functions.rateProvider0().call()
    rate_provider_1 = pool_contract.functions.rateProvider1().call()

    return RateProviders(
        rate_provider_0=rate_provider_0, rate_provider_1=rate_provider_1
    )


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

    # for key, value in params.model_dump().items():
    #     value = Decimal(value) / Decimal(1e18)
    #     print(f"{key}: {value}")

    # for key, value in d.model_dump().items():
    #     value = Decimal(value) / Decimal(1e38)
    #     print(f"{key}: {value}")

    return params, d
