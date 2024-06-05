import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from integers.blockchain.get_vault_data import get_initial_token_balances
from integers.blockchain.get_pool_data import (
    get_pool_id,
    get_effective_amount_in_percentage,
    get_eclp_parmas,
)
from integers.offsets import virtual_offset_0, virtual_offset_1
from amm import solve_quadratic_swap
from invariant import calculate_invariant_with_error
from data.pool_data import process_invariant

from integers.schemas.pool import Params, DerivedParams, R, Midpoint, Vector2


"""
Standarize the following:

- ✅ inital token balances (hard code)
- ✅ invariant (hard code)
- ✅ eclp params (hard code)
"""


def get_offsets(p: Params, d: DerivedParams, r: R) -> Midpoint:
    """Get the midpoint of the ellipse."""

    return Midpoint(
        a=virtual_offset_0(p=p, d=d, r=r), b=virtual_offset_1(p=p, d=d, r=r)
    )


def start_simulation() -> None:
    # Read contract data
    pool_id = get_pool_id()
    contract_token_balances = get_initial_token_balances(pool_id)
    f = get_effective_amount_in_percentage()
    p, d = get_eclp_parmas()

    # Use token balances and params to calculate invariant
    invariant, err = calculate_invariant_with_error(
        balances=contract_token_balances, p=p, d=d
    )
    processed_r = process_invariant(invariant=invariant, err=err)

    # Precompute virtual offsets
    midpoint = get_offsets(p=p, d=d, r=processed_r)

    # calcuate amount out
    x_in = 1000e18

    # λ: int, new_x_bal: int, r: R, ab: Midpoint, p: Params, d: DerivedParams
    new_y_bal = solve_quadratic_swap(
        λ=p.λ,
        new_x_bal=contract_token_balances.x_0 + x_in,
        s=p.s,
        c=p.c,
        r=processed_r,
        ab=midpoint,
        tauBeta=Vector2(x=d.tau_beta_x, y=d.tau_beta_y),
        dSq=d.d_sq,
    )

    amount_out = contract_token_balances.y_0 - new_y_bal

    print("\n\ny_out:", amount_out)


if __name__ == "__main__":
    start_simulation()
