ONE = 1e18
ONE_XP = 1e38


def div_xp_u(a, b):
    return (a * ONE_XP) // b


def mul_down_mag_u(a, b):
    return (a * b) // ONE


def mul_up_mag_u(a, b):
    product = a * b
    if product > 0:
        return ((product - 1) // ONE) + 1
    elif product < 0:
        return ((product + 1) // ONE) - 1
    return 0


def mul_up_xp_to_np_u(a, b):
    b1 = b // int(1e19)
    b2 = b % int(1e19)
    prod1 = a * b1
    prod2 = a * b2
    return (
        ((prod1 + prod2 // int(1e19)) // int(1e19))
        if prod1 <= 0 and prod2 <= 0
        else ((prod1 + prod2 // int(1e19) - 1) // int(1e19)) + 1
    )


def div_down_mag_u(a, b):
    if b == 0:
        raise ZeroDivisionError("Division by zero")
    return (a * ONE) // b


def div_up_mag_u(a, b):
    if b == 0:
        raise ZeroDivisionError("Division by zero")
    if a == 0:
        return 0
    if b < 0:
        b = -b
        a = -a
    if a > 0:
        return ((a * ONE - 1) // b) + 1
    return ((a * ONE + 1) // b) - 1


def mul_down_xp_to_np_u(a, b):
    b1 = b // int(1e19)
    b2 = b % int(1e19)
    prod1 = a * b1
    prod2 = a * b2
    return (
        ((prod1 + prod2 // int(1e19)) // int(1e19))
        if prod1 >= 0 and prod2 >= 0
        else ((prod1 + prod2 // int(1e19) + 1) // int(1e19)) - 1
    )


def mul_xp_u(a, b):
    return (a * b) // ONE_XP
