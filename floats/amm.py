import sys
import os
from math import sqrt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from schemas.pool import Params, R, Midpoint
from schemas.vault import VaultTokenInfo


def get_y_out_given_x_in(
    x_in: float, bals: VaultTokenInfo, p: Params, r: R, midpoint: Midpoint, f: float
) -> float:
    """Calculates the amount out given amount in."""

    # constuct x'
    x_in_after_fees = f * x_in
    new_x_bal = bals.x_0 + x_in_after_fees
    xp = new_x_bal - midpoint.a

    # squared terms
    r_sq = r.x**2
    s_sq = p.s**2
    λ_sq = p.λ**2
    xp_sq = xp**2

    # construct first term
    λ_bar = 1 - (1 / λ_sq)
    term_1 = (-xp) * λ_bar * p.s * p.c

    # construct the square root term
    s_term = 1 - λ_bar * s_sq

    quotient_1 = xp_sq / λ_sq

    radicand = r_sq * s_term - quotient_1

    root_term = sqrt(radicand)

    # construct quotient term
    quotient_2 = (term_1 - root_term) / s_term

    # construct final term
    post_bal = quotient_2 + midpoint.b

    return bals.y_0 - post_bal


def get_dy_over_dx(
    x_in: float, bals: VaultTokenInfo, p: Params, r: R, midpoint: Midpoint, f: float
) -> float:
    """Calculates the derivative of y with respect to x."""

    # constuct x'
    x_in_after_fees = f * x_in
    new_x_bal = bals.x_0 + x_in_after_fees
    xp = new_x_bal - midpoint.a

    # squared terms
    r_sq = r.x**2
    s_sq = p.s**2
    λ_sq = p.λ**2
    xp_sq = xp**2

    # construct first term
    λ_bar = 1 - (1 / λ_sq)

    # construct s term
    s_term = 1 - λ_bar * s_sq

    term_1 = f / s_term

    term_2 = λ_bar * p.s * p.c

    # construct root trem
    radicand = r_sq * s_term - (xp_sq / λ_sq)
    root_term = sqrt(radicand)

    denominator = λ_sq * root_term

    return term_1 * (term_2 - (xp / denominator))
