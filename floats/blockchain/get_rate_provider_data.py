import os
import sys

from web3 import Web3
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from abis.sdai_rate_provider import ABI as RATE_PROVIDER_ABI
from schemas.pool import RateProviders
from schemas.rate_providers import Rates

# For Standarization
from constants import X_0, Y_0, ZERO_ADDRESS, RATE_0

load_dotenv(".env")


def get_rates(rate_providers: RateProviders) -> Rates:
    """Returns the starting balances for both of the tokens in the pool."""

    web3 = Web3(Web3.HTTPProvider(os.environ.get("ETHEREUM_RPC")))

    if rate_providers.rate_provider_0 != ZERO_ADDRESS:
        rate_provider_0_contract = web3.eth.contract(
            address=rate_providers.rate_provider_0, abi=RATE_PROVIDER_ABI
        )
        # rate_0 = rate_provider_0_contract.functions.getRate().call()
        rate_0 = RATE_0
    else:
        rate_0 = 1

    if rate_providers.rate_provider_1 != ZERO_ADDRESS:

        rate_provider_1_contract = web3.eth.contract(
            address=rate_providers.rate_provider_1, abi=RATE_PROVIDER_ABI
        )

        rate_1 = rate_provider_1_contract.functions.getRate().call()
    else:
        rate_1 = 1

    return Rates(rate_0=rate_0, rate_1=rate_1)
