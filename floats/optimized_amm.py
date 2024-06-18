import sys
import os
from math import sqrt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def eclp(
    input: float,
    translated_reserve_out: float,
    λ_sq: float,
    input_scale: float,
    rate_out: float,
    pc1: float,
    pc2: float,
    pc3: float,
    pc4: float,
    pc5: float
) -> float:
    """Calculates the amount out given amount in."""

    # constuct x' and its square
    xp = pc1 + input * input_scale
    xp_sq = xp**2

    # construct first product term
    prod_term = (-xp) * pc2

    # construct the square root term
    root_term = sqrt(pc4 - (xp_sq / λ_sq))

    # construct quotient term
    quotient = (prod_term - root_term) / pc3

    # construct final term
    # we have a case where it's already correct for input token (multiplication case)
    # it's wrong for output token (division case)
    amt_out = (translated_reserve_out - quotient) / rate_out

    """Dervivative"""
    
    denominator = λ_sq * root_term

    grad = pc5 * (pc2 - (xp / denominator))

    return amt_out, grad