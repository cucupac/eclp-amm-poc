import os
import sys
from typing import Tuple
from decimal import Decimal

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schemas.pool import Params, DerivedParams, R


def process_elcp_params(p: Params, d: DerivedParams) -> Tuple[Params, DerivedParams]:
    params_dict = p.model_dump()
    for key in params_dict:
        params_dict[key] = Decimal(params_dict[key]) / Decimal(1e18)

    derived_params_dict = d.model_dump()
    for key in derived_params_dict:
        derived_params_dict[key] = Decimal(derived_params_dict[key]) / Decimal(1e38)

    return Params(**params_dict), DerivedParams(**derived_params_dict)


def process_invariant(invariant: int) -> R:
    """Does not calculate error."""
    return R(x=Decimal(invariant) / Decimal(1e18), y=Decimal(invariant) / Decimal(1e18))
