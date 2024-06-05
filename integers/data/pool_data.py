from integers.schemas.pool import R


def process_invariant(invariant: int, err: int) -> R:

    return R(x=invariant + 2 * err, y=invariant)
