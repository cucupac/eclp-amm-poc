import sys
import os
from math import sqrt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def eclp(
    input: float,
    reserve_out: float,
    λ_sq: float,
    f: float,
    offset: float,
    pc1: float,
    pc2: float,
    pc3: float,
    pc4: float,
) -> float:
    """Calculates the amount out given amount in."""

    # constuct x' and its square
    xp = pc1 + f * input
    xp_sq = xp**2

    # construct first product term
    term_1 = (-xp) * pc2

    # construct the square root term
    term_2 = sqrt(pc4 - (xp_sq / λ_sq))

    # construct quotient term
    quotient = (term_1 - term_2) / pc3

    # construct final term
    post_out_bal = quotient + offset

    return reserve_out - post_out_bal


def derivative(
    input: float,
    λ_sq: float,
    f: float,
    pc1: float,
    pc2: float,
    pc4: float,
    pc5: float
) -> float:
    
    # constuct x' and its square
    xp = pc1 + f * input
    xp_sq = xp**2

    # construct root term
    root_term = sqrt(pc4 - (xp_sq / λ_sq))

    denominator = λ_sq * root_term

    return pc5 * (pc2 - (xp / denominator))
