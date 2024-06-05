import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from schemas.pool import Params, DerivedParams, R


# NOTE: since x.tau_beta_x is positive, we'll have to calculate the error.
def virtual_offset_0(p: Params, d: DerivedParams, r: R) -> int:
    termXp = d.tau_beta_x / d.d_sq

    if d.tau_beta_x > 0:
        # Use over estimated invariant with included error
        a = r.x * p.λ * p.c * termXp
    else:
        # Use the calculated invariant
        a = r.y * p.λ * p.c * termXp

    a += r.x * p.s * (d.tau_beta_y / d.d_sq)

    return a


# NOTE: since x.tau_alpha_x is positive, we'll have to calculate the error.
def virtual_offset_1(p: Params, d: DerivedParams, r: R) -> int:

    termXp = d.tau_alpha_x / d.d_sq

    if d.tau_alpha_x < 0:
        b = r.x * p.λ * p.s * (-termXp)
    else:
        b = (-r.y) * p.λ * p.s * (termXp)

    b += r.x * p.c * (d.tau_alpha_y / d.d_sq)

    return b
