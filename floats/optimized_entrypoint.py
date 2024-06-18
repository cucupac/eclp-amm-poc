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
from floats.optimized_amm import eclp
from data.pool_data import process_elcp_params, process_invariant
from data.vault_data import get_token_balances
from data.rate_provider_data import process_rates
from floats.invariant import calculate_invariant

from schemas.pool import Params, DerivedParams, R, Midpoint, AMMParams
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


def get_token_info(
    pool_id: str, processed_rates: Rates
) -> Tuple[VaultTokenInfo, TokenBalances]:
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
    print("y_0 balance:", y_0)
    print("invariant:", r)
    print("calculated amount out:", amt_out)
    print("calculated dy/dx:", grad, "\n\n")


def get_trading_function_inputs(
    x_in_y_out: bool,
    processed_p: Params,
    processed_rates: Rates,
    midpoint: Midpoint,
    processed_r: R,
    processed_token_balances: TokenBalances,
) -> Tuple[float, float, float, float, float]:

    f = get_effective_amount_in_percentage()

    if x_in_y_out:
        """Execute trade: x in, y out."""
        # assign input
        x_in = 1000
        input = x_in

        # assign rates
        rate_in = processed_rates.rate_0
        rate_out = processed_rates.rate_1
        rate_scale = processed_rates.rate_0 * processed_rates.rate_1

        # assign output
        reserve_out = processed_token_balances.y_0

        # assign rotation params
        rot_param_1 = processed_p.s
        rot_param_2 = processed_p.c

        # assign offset
        offset = midpoint.b

        # calculate λ_bar
        λ_bar = 1 - (1 / processed_p.λ**2)

        # calculate pc terms
        reserve_in = processed_token_balances.x_0
        pc_1 = reserve_in - midpoint.a
    else:
        """Execute trade: y in, x out."""
        # assign input
        y_in = 1000
        input = y_in

        # assign rate
        rate_in = processed_rates.rate_1
        rate_out = processed_rates.rate_0
        rate_scale = 1 / (processed_rates.rate_0 * processed_rates.rate_1)

        # assign output
        reserve_out = processed_token_balances.x_0

        # assign rotation params
        rot_param_1 = processed_p.c
        rot_param_2 = processed_p.s

        # assign offset
        offset = midpoint.a

        # calculate λ_bar
        λ_bar = 1 - (1 / processed_p.λ**2)

        # calculate pc terms
        reserve_in = processed_token_balances.y_0
        pc_1 = reserve_in - midpoint.b


    # Common
    pc_2 = λ_bar * rot_param_1 * rot_param_2
    pc_3 = 1 - λ_bar * rot_param_1**2
    pc_4 = processed_r.x**2 * pc_3
    pc_5 = (f / pc_3) * rate_scale
    translated_reserve_out = reserve_out - offset
    input_scale = rate_in * f

    return AMMParams(
        input=input,
        translated_reserve_out=translated_reserve_out,
        λ_sq=processed_p.λ**2,
        input_scale=input_scale,
        rate_out=rate_out,
        pc1=pc_1,
        pc2=pc_2,
        pc3=pc_3,
        pc4=pc_4,
        pc5=pc_5,
    )


def start_simulation() -> None:
    """Gather information needed for calculations."""
    # Get token balances
    pool_id = get_pool_id()

    # Get rates
    processed_rates = get_token_rates()

    # Get token balance info
    scaled_token_info, processed_token_balances = get_token_info(
        pool_id=pool_id, processed_rates=processed_rates
    )

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

    """Get AMM parameters."""
    x_in_y_out = False
    amm_params = get_trading_function_inputs(
        x_in_y_out=x_in_y_out,
        processed_p=processed_p,
        processed_rates=processed_rates,
        midpoint=midpoint,
        processed_r=processed_r,
        processed_token_balances=processed_token_balances,
    )

    """Execute trade."""
    # NOTE: balances are float amounts (divided by decimals)
    amt_out, grad = eclp(
        input=amm_params.input,
        translated_reserve_out=amm_params.translated_reserve_out,
        λ_sq=processed_p.λ**2,
        input_scale=amm_params.input_scale,
        rate_out=amm_params.rate_out,
        pc1=amm_params.pc1,
        pc2=amm_params.pc2,
        pc3=amm_params.pc3,
        pc4=amm_params.pc4,
        pc5=amm_params.pc5,
    )

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
