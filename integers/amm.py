import sys
import os
from math import sqrt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from schemas.pool import R, Midpoint, Vector2, QParams
from integer_math.signed_fixed_point import (
    ONE_XP,
    div_down_mag_u,
    mul_up_mag_u,
    mul_down_mag_u,
    mul_up_xp_to_np_u,
    div_up_mag_u,
    mul_xp_u,
    div_xp_u,
    mul_down_xp_to_np_u,
)


def solve_quadratic_swap(
    λ: int,
    new_x_bal: int,
    s: int,
    c: int,
    r: R,
    ab: Midpoint,
    tauBeta: Vector2,
    dSq: int,
) -> int:

    λ_bar_x = ONE_XP - div_down_mag_u(div_down_mag_u(ONE_XP, λ), λ)
    λ_bar_y = ONE_XP - div_up_mag_u(div_up_mag_u(ONE_XP, λ), λ)

    λ_bar = Vector2(x=λ_bar_x, y=λ_bar_y)

    xp = new_x_bal - ab.a

    q = QParams()
    if xp > 0:
        q.b = mul_up_xp_to_np_u(
            mul_down_mag_u(mul_down_mag_u(-xp, s), c), div_xp_u(λ_bar.y, dSq)
        )
    else:
        q.b = mul_up_xp_to_np_u(
            mul_up_mag_u(mul_up_mag_u(-xp, s), c), div_xp_u(λ_bar.x, dSq) + 1
        )

    s_term_x = div_xp_u(mul_down_mag_u(mul_down_mag_u(λ_bar.y, s), s), dSq)
    s_term_y = div_xp_u(mul_up_mag_u(mul_up_mag_u(λ_bar.x, s), s), dSq + 1) + 1
    s_term = Vector2(x=ONE_XP - s_term_x, y=ONE_XP - s_term_y)

    # calculate the square root term
    r_y_sq = r.y**2
    λ_sq = λ**2
    xp_sq = xp**2
    quotient_1 = xp_sq / λ_sq
    radicand = r_y_sq * s_term.y - quotient_1

    q.c = -calc_xp_xp_div_lambda_lambda(
        x=new_x_bal, r=r, λ=λ, s=s, c=c, tauBeta=tauBeta, dSq=dSq
    )
    q.c = q.c + mul_down_xp_to_np_u(mul_down_mag_u(r.y, r.y), s_term.y)

    if q.c > 0:
        q.c = sqrt(q.c) * 1e9  # scale up to match contracts at this point.
    else:
        q.c = 0

    if q.b - q.c > 0:
        q.a = mul_up_xp_to_np_u(q.b - q.c, div_xp_u(ONE_XP, s_term.y) + 1)
    else:
        q.a = mul_up_xp_to_np_u(q.b - q.c, div_xp_u(ONE_XP, s_term.x))

    return q.a + ab.b


def calc_xp_xp_div_lambda_lambda(
    x: int, r: R, λ: int, s: int, c: int, tauBeta: Vector2, dSq: int
) -> int:

    sqVars = Vector2(x=mul_xp_u(dSq, dSq), y=mul_up_mag_u(r.x, r.x))

    q = QParams()
    termXp = div_xp_u(mul_xp_u(tauBeta.x, tauBeta.y), sqVars.x)
    if termXp > 0:
        q.a = mul_up_xp_to_np_u(
            mul_up_mag_u(mul_up_mag_u(sqVars.y, 2 * s), c), termXp + 7
        )
    else:
        q.a = mul_up_xp_to_np_u(
            mul_down_mag_u(mul_down_mag_u(mul_down_mag_u(r.y, r.y), 2 * s), c), termXp
        )

    if tauBeta.x < 0:
        q.b = mul_up_xp_to_np_u(
            mul_up_mag_u(mul_up_mag_u(r.x, x), 2 * c), div_xp_u(-tauBeta.x, dSq) + 3
        )
    else:
        q.b = mul_up_xp_to_np_u(
            mul_down_mag_u(mul_down_mag_u(-r.y, x), 2 * c), div_xp_u(tauBeta.x, dSq)
        )

    q.a = q.a + q.b

    termXp = div_xp_u(mul_xp_u(tauBeta.y, tauBeta.y), sqVars.x) + 7
    q.b = mul_up_xp_to_np_u(mul_up_mag_u(mul_up_mag_u(sqVars.y, s), s), termXp)

    q.c = mul_up_xp_to_np_u(
        mul_down_mag_u(mul_down_mag_u(-r.y, x), 2 * s), div_xp_u(tauBeta.y, dSq)
    )

    q.b = q.b + q.c + mul_up_mag_u(x, x)
    if q.b > 0:
        q.b = div_up_mag_u(q.b, λ)
    else:
        q.b = div_down_mag_u(q.b, λ)

    q.a = q.a + q.b

    if q.a > 0:
        q.a = div_up_mag_u(q.a, λ)
    else:
        q.a = div_down_mag_u(q.a, λ)

    termXp = div_xp_u(mul_xp_u(tauBeta.x, tauBeta.x), sqVars.x) + 7

    val = mul_up_mag_u(mul_up_mag_u(sqVars.y, c), c)

    return mul_up_xp_to_np_u(val, termXp) + q.a
