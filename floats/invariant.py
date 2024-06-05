import sys
import os
from math import sqrt

import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schemas.vault import VaultTokenInfo
from schemas.pool import Params


def get_A(p: Params) -> np.ndarray:
    return np.array([[p.c / p.λ, -p.s / p.λ], [p.s, p.c]])


def get_A_INV(p: Params) -> np.ndarray:
    return np.array([[p.c * p.λ, p.s], [-p.s * p.λ, p.c]])


def get_t(x_0: int, y_0: int) -> np.ndarray:
    return np.array([x_0, y_0])


def get_e_x() -> np.ndarray:
    return np.array([1, 0])


def get_e_y() -> np.ndarray:
    return np.array([0, 1])


def zeta(pxe: int, p: Params) -> int:

    A = get_A(p=p)
    e_x = get_e_x()
    e_y = get_e_y()

    matrix_T = np.array([[-1], [pxe]], dtype=float)

    product = np.matmul(A, matrix_T)

    numerator = np.dot(e_y, product)
    denominator = np.dot(-e_x, product)

    return (numerator / denominator).item()


def eta(pxc: int) -> np.ndarray:

    matrix = np.array([[pxc], [1]], dtype=float)

    scalar = 1 / sqrt(1 + pxc**2)

    return scalar * matrix


def tau(pxe: int, p: Params) -> np.ndarray:

    pxc = zeta(pxe=pxe, p=p)
    return eta(pxc=pxc)


def chi(alpha: int, beta: int, p: Params) -> np.ndarray:
    A_INV = get_A_INV(p=p)
    ex = get_e_x()
    ey = get_e_y()

    x_prod = np.matmul(A_INV, tau(pxe=beta, p=p))
    y_prod = np.matmul(A_INV, tau(pxe=alpha, p=p))

    x = np.dot(ex, x_prod).item()
    y = np.dot(ey, y_prod).item()

    return np.array([x, y])


def calculate_invariant(x_0: float, y_0: float, p: Params) -> float:

    A = get_A(p=p)
    t = get_t(x_0=x_0, y_0=y_0)

    X = chi(alpha=p.alpha, beta=p.beta, p=p)

    term_1 = np.dot(np.matmul(A, t), np.matmul(A, X))

    root_sub_term_1 = (np.dot(np.matmul(A, t), np.matmul(A, X))) ** 2
    root_sub_term_2 = np.dot(np.matmul(A, X), np.matmul(A, X)) - 1
    root_sub_term_3 = np.dot(np.matmul(A, t), np.matmul(A, t))
    radicand = root_sub_term_1 - root_sub_term_2 * root_sub_term_3
    term_2 = sqrt(radicand)

    term_3 = np.dot(np.matmul(A, X), np.matmul(A, X)) - 1

    return (term_1 + term_2) / term_3
