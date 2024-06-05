import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schemas.rate_providers import Rates


def process_rates(rates: Rates) -> Rates:
    if rates.rate_0 != 1:
        rates.rate_0 = rates.rate_0 / 1e18

    if rates.rate_1 != 1:
        rates.rate_1 = rates.rate_1 / 1e18
    return rates
