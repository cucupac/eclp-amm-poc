import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from schemas.pool import Params, DerivedParams, R


def virtual_offset_0(p: Params, d: DerivedParams, r: R) -> float:
    termXp = d.tau_beta_x / d.d_sq

    a = r.x * p.λ * p.c * termXp

    a += r.x * p.s * (d.tau_beta_y / d.d_sq)

    return a


def virtual_offset_1(p: Params, d: DerivedParams, r: R) -> float:

    termXp = d.tau_alpha_x / d.d_sq

    b = r.x * p.λ * p.s * (-termXp)

    b += r.x * p.c * (d.tau_alpha_y / d.d_sq)

    return b
