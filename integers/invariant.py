import sys
import os
from typing import Tuple
from math import sqrt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from integer_math.signed_fixed_point import (
    ONE_XP,
    div_down_mag_u,
    mul_up_mag_u,
    mul_down_mag_u,
    mul_xp_u,
    div_xp_u,
    mul_down_xp_to_np_u,
    div_up_mag_u,
    mul_up_xp_to_np_u,
)
from schemas.pool import Params, DerivedParams
from schemas.vault import TokenBalances
from constants import SQRT_MULTIPLIER


def calculate_invariant_with_error(
    balances: TokenBalances, p: Params, d: DerivedParams
) -> int:
    """Calculates invariant and error."""

    x = balances.x_0
    y = balances.y_0

    at_a_chi = calc_at_a_chi(x, y, p, d)
    sqrt, err = calc_invariant_sqrt(x, y, p, d)

    if sqrt > 0:
        err = div_up_mag_u(err + 1, 2 * sqrt)
    else:
        err = sqrt(err) * SQRT_MULTIPLIER if err > 0 else 0

    err = (mul_up_mag_u(p.λ, x + y) // ONE_XP + err + 1) * 20

    mul_denominator = div_xp_u(ONE_XP, calc_a_chi_a_chi_in_xp(p, d) - ONE_XP)

    invariant = mul_down_xp_to_np_u(at_a_chi + sqrt - err, mul_denominator)

    err = mul_up_xp_to_np_u(err, mul_denominator)

    err = (
        err
        + ((mul_up_xp_to_np_u(invariant, mul_denominator) * ((p.λ * p.λ) // 1e36)) * 40)
        // ONE_XP
        + 1
    )

    return invariant, err


def calc_at_a_chi(x: int, y: int, p: Params, d: DerivedParams) -> int:
    dSq2 = mul_xp_u(d.d_sq, d.d_sq)

    termXp = div_down_mag_u(div_down_mag_u(d.w, p.λ) + d.z, div_xp_u(p.λ, dSq2))

    val = mul_down_xp_to_np_u(mul_down_mag_u(x, p.c) - mul_down_mag_u(y, p.s), termXp)

    termNp = mul_down_mag_u(mul_down_mag_u(x, p.λ), p.s) + mul_down_mag_u(
        mul_down_mag_u(y, p.λ), p.c
    )
    val = val + mul_down_xp_to_np_u(termNp, div_xp_u(d.u, dSq2))

    termNp = mul_down_mag_u(x, p.s) + mul_down_mag_u(y, p.c)
    return val + mul_down_xp_to_np_u(termNp, div_xp_u(d.v, d.d_sq))


def calc_invariant_sqrt(x: int, y: int, p: Params, d: DerivedParams) -> Tuple[int, int]:
    """"""

    val = calc_min_at_x_a_chi_y_plus_at_a_sq(
        x, y, p, d
    ) + calc_2_at_x_at_y_chi_x_a_chi_y(x, y, p, d)
    val = val + calc_min_at_y_chi_x_sq_plus_at_y_sq(x, y, p, d)

    err = (mul_up_mag_u(x, x) + mul_up_mag_u(y, y)) // ONE_XP

    val = sqrt(val) * SQRT_MULTIPLIER if val > 0 else 0

    return val, err


def calc_min_at_x_a_chi_y_plus_at_a_sq(
    x: int, y: int, p: Params, d: DerivedParams
) -> int:
    """"""

    termNp = mul_up_mag_u(mul_up_mag_u(mul_up_mag_u(x, x), p.c), p.c) + mul_up_mag_u(
        mul_up_mag_u(mul_up_mag_u(y, y), p.s), p.s
    )
    termNp = termNp - mul_down_mag_u(mul_down_mag_u(mul_down_mag_u(x, y), p.c * 2), p.s)

    termXp = (
        mul_xp_u(d.u, d.u)
        + div_down_mag_u(mul_xp_u(2 * d.u, d.v), p.λ)
        + div_down_mag_u(div_down_mag_u(mul_xp_u(d.v, d.v), p.λ), p.λ)
    )
    termXp = div_xp_u(
        termXp, mul_xp_u(mul_xp_u(mul_xp_u(d.d_sq, d.d_sq), d.d_sq), d.d_sq)
    )
    val = mul_down_xp_to_np_u(-termNp, termXp)

    return val + mul_down_xp_to_np_u(
        div_down_mag_u(div_down_mag_u(termNp - 9, p.λ), p.λ), div_xp_u(ONE_XP, d.d_sq)
    )


def calc_2_at_x_at_y_chi_x_a_chi_y(x: int, y: int, p: Params, d: DerivedParams) -> int:

    termNp = mul_down_mag_u(
        mul_down_mag_u(mul_down_mag_u(x, x) - mul_up_mag_u(y, y), 2 * p.c), p.s
    )
    xy = mul_down_mag_u(y, 2 * x)
    termNp = (
        termNp
        + mul_down_mag_u(mul_down_mag_u(xy, p.c), p.c)
        - mul_down_mag_u(mul_down_mag_u(xy, p.s), p.s)
    )

    termXp = mul_xp_u(d.z, d.u) + div_down_mag_u(
        div_down_mag_u(mul_xp_u(d.w, d.v), p.λ), p.λ
    )
    termXp = termXp + div_down_mag_u((mul_xp_u(d.w, d.u) + mul_xp_u(d.z, d.v)), p.λ)
    termXp = div_xp_u(
        termXp, mul_xp_u(mul_xp_u(mul_xp_u(d.d_sq, d.d_sq), d.d_sq), d.d_sq)
    )

    return mul_down_xp_to_np_u(termNp, termXp)


def calc_min_at_y_chi_x_sq_plus_at_y_sq(
    x: int, y: int, p: Params, d: DerivedParams
) -> int:

    termNp = mul_up_mag_u(mul_up_mag_u(mul_up_mag_u(x, x), p.s), p.s) + mul_up_mag_u(
        mul_up_mag_u(mul_up_mag_u(y, y), p.c), p.c
    )

    termNp = termNp + mul_up_mag_u(mul_up_mag_u(mul_up_mag_u(x, y), p.s * 2), p.c)

    termXp = mul_xp_u(d.z, d.z) + div_down_mag_u(
        div_down_mag_u(mul_xp_u(d.w, d.w), p.λ), p.λ
    )
    termXp = termXp + div_down_mag_u(mul_xp_u(2 * d.z, d.w), p.λ)
    termXp = div_xp_u(
        termXp, mul_xp_u(mul_xp_u(mul_xp_u(d.d_sq, d.d_sq), d.d_sq), d.d_sq)
    )

    val = mul_down_xp_to_np_u(-termNp, termXp)

    return val + mul_down_xp_to_np_u(termNp - 9, div_xp_u(ONE_XP, d.d_sq))


def calc_a_chi_a_chi_in_xp(p: Params, d: DerivedParams) -> int:

    d_sq_3 = mul_xp_u(mul_xp_u(d.d_sq, d.d_sq), d.d_sq)

    val = mul_up_mag_u(p.λ, div_xp_u(mul_xp_u(2 * d.u, d.v), d_sq_3))

    val = val + mul_up_mag_u(
        mul_up_mag_u((div_xp_u(mul_xp_u(d.u + 1, d.u + 1), d_sq_3)), p.λ), p.λ
    )

    val = val + div_xp_u(mul_xp_u(d.v, d.v), d_sq_3)

    termXp = div_up_mag_u(d.w, p.λ) + d.z

    return val + div_xp_u(mul_xp_u(termXp, termXp), d_sq_3)
