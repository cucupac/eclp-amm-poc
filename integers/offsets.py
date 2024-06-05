import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from schemas.pool import Params, DerivedParams, R
from integer_math.signed_fixed_point import (
    mul_up_mag_u,
    mul_down_mag_u,
    mul_up_xp_to_np_u,
    div_xp_u,
)


def virtual_offset_0(p: Params, d: DerivedParams, r: R) -> int:
    termXp = div_xp_u(d.tau_beta_x, d.d_sq)

    if d.tau_beta_x > 0:
        a = mul_up_mag_u(r.x, p.λ)
        a = mul_up_mag_u(a, p.c)
        a = mul_up_xp_to_np_u(a, termXp)
    else:
        a = mul_down_mag_u(r.y, p.λ)
        a = mul_down_mag_u(a, p.c)
        a = mul_up_xp_to_np_u(a, termXp)

    term = mul_up_mag_u(r.x, p.s)
    quotient = div_xp_u(d.tau_beta_y, d.d_sq)
    operand = mul_up_xp_to_np_u(term, quotient)

    a += operand

    return a


def virtual_offset_1(p: Params, d: DerivedParams, r: R) -> int:
    termXp = div_xp_u(d.tau_alpha_x, d.d_sq)

    if d.tau_alpha_x < 0:
        b = mul_up_mag_u(r.x, p.λ)
        b = mul_up_mag_u(b, p.s)
        b = mul_up_xp_to_np_u(b, -termXp)
    else:
        b = mul_down_mag_u(-r.y, p.λ)
        b = mul_down_mag_u(b, p.s)
        b = mul_up_xp_to_np_u(b, termXp)

    term = mul_up_mag_u(r.x, p.c)
    quotient = div_xp_u(d.tau_alpha_y, d.d_sq)
    operand = mul_up_xp_to_np_u(term, quotient)

    b += operand

    return b
