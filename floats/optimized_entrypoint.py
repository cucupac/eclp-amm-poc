import sys
import os
from typing import Tuple

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from blockchain.get_vault_data import get_initial_token_balances
from blockchain.get_pool_data import (
    get_pool_id,
    get_effective_amount_in_percentage,
    get_eclp_parmas,
    get_rate_providers,
)
from blockchain.get_token_data import get_token_decimals
from blockchain.get_rate_provider_data import get_rates
from floats.offsets import virtual_offset_0, virtual_offset_1
from floats.optimized_amm import eclp, derivative
from data.pool_data import process_elcp_params, process_invariant
from data.vault_data import get_token_balances
from data.rate_provider_data import process_rates
from floats.invariant import calculate_invariant

from schemas.pool import Params, DerivedParams, R, Midpoint
from schemas.vault import VaultTokenInfo, TokenBalances
from schemas.rate_providers import Rates


def get_offsets(p: Params, d: DerivedParams, r: R) -> Midpoint:
    """Get the midpoint of the ellipse."""

    return Midpoint(
        a=virtual_offset_0(p=p, d=d, r=r), b=virtual_offset_1(p=p, d=d, r=r)
    )


def scale_raw_token_balances(
    token_info_with_decimals: VaultTokenInfo,
) -> VaultTokenInfo:
    """Scales token balances up to 18 decimals."""
    scaled_token_info = token_info_with_decimals.model_copy()

    x_scaling_factor = 10 ** (18 - token_info_with_decimals.x_0.decimals)
    y_scaling_factor = 10 ** (18 - token_info_with_decimals.y_0.decimals)
    scaled_token_info.x_0.amount = scaled_token_info.x_0.amount * x_scaling_factor
    scaled_token_info.y_0.amount = scaled_token_info.y_0.amount * y_scaling_factor
    return scaled_token_info


def get_token_rates() -> Rates:
    rate_providers = get_rate_providers()
    rates = get_rates(rate_providers=rate_providers)
    return process_rates(rates=rates)


def get_token_info(pool_id: str, processed_rates: Rates) -> Tuple[VaultTokenInfo, TokenBalances]:
    """Returns token balances scaled to 18 decimals and unscaled."""

    # Get token information
    token_info = get_initial_token_balances(pool_id=pool_id)

    # Apply rates to balances
    token_info.x_0.amount *= processed_rates.rate_0
    token_info.y_0.amount *= processed_rates.rate_1

    # Process token information
    token_info_with_decimals = get_token_decimals(vault_token_info=token_info)
    processed_token_balances = get_token_balances(tokens=token_info_with_decimals)

    # Scale token balances
    scaled_token_info = scale_raw_token_balances(
        token_info_with_decimals=token_info_with_decimals
    )

    return scaled_token_info, processed_token_balances


def print_results(
    amt_out: float, grad: float, r: float, x_0: float, y_0: float
) -> None:
    print("\n\nx_0 balance:", x_0)
    print("\n\ny_0 balance:", y_0)
    print("\n\ninvariant:", r)
    print("\n\ncalculated amount out:", amt_out)
    print("\n\ncalculated dy/dx:", grad, "\n\n")


def start_simulation() -> None:
    """Gather information needed for calculations."""
    # Get token balances
    pool_id = get_pool_id()

    # Get rates
    processed_rates = get_token_rates()

    # Get token balance info
    scaled_token_info, processed_token_balances = get_token_info(pool_id=pool_id, processed_rates=processed_rates)

    # Get pool params
    p, d = get_eclp_parmas()
    processed_p, processed_d = process_elcp_params(p=p, d=d)

    """Cacluate invariant."""
    # NOTE: balances are scaled up to 18 decimals
    processed_r = process_invariant(
        invariant=calculate_invariant(
            x_0=scaled_token_info.x_0.amount,
            y_0=scaled_token_info.y_0.amount,
            p=processed_p,
        )
    )

    """Cacluate midpoint."""
    midpoint = get_offsets(p=processed_p, d=processed_d, r=processed_r)

    """Assign the input token amount."""
    x_in = 1000
    x_in *= processed_rates.rate_0  # apply rates
    f = get_effective_amount_in_percentage()

    """Execute trade: x in, y out."""
    # NOTE: balances are float amounts (divided by decimals)

    # assign input
    input = x_in

    # assign rotation params
    rot_param_1 = processed_p.s
    rot_param_2 = processed_p.c

    # assign offset
    offset = midpoint.b

    # calculate λ_bar
    λ_bar = 1 - (1 / processed_p.λ ** 2)

    # calculate pc terms
    reserve_in = processed_token_balances.x_0
    pc_1 = reserve_in - midpoint.a
    pc_2 = λ_bar * rot_param_1 * rot_param_2
    pc_3 = 1 - λ_bar * rot_param_1 ** 2
    pc_4 = processed_r.x ** 2 * pc_3
    pc_5 = f / pc_3

    # calculate amount out
    amt_out = eclp(
        input=input,
        reserve_out=processed_token_balances.y_0,
        λ_sq=processed_p.λ**2,
        f=f,
        offset=offset,
        pc1=pc_1,
        pc2=pc_2,
        pc3=pc_3,
        pc4=pc_4,
    )

    """Calculate spot price."""
    grad = derivative(
        input=input,
        λ_sq=processed_p.λ**2,
        f=f,
        pc1=pc_1,
        pc2=pc_2,
        pc4=pc_4,
        pc5=pc_5
    )

    # Adjust price
    if processed_rates.rate_0 != 1:
        grad *= processed_rates.rate_0

    if processed_rates.rate_1 != 1:
        grad *= processed_rates.rate_1

    """Print Results."""
    print_results(
        amt_out=amt_out,
        grad=grad,
        r=processed_r,
        x_0=scaled_token_info.x_0.amount,
        y_0=scaled_token_info.y_0.amount,
    )


if __name__ == "__main__":
    start_simulation()