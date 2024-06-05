from typing import Optional

from pydantic import BaseModel

"""INTEGERS"""


class Params(BaseModel):
    alpha: int
    beta: int
    c: int
    s: int
    λ: int


class DerivedParams(BaseModel):
    tau_alpha_x: int
    tau_alpha_y: int
    tau_beta_x: int
    tau_beta_y: int
    u: int
    v: int
    w: int
    z: int
    d_sq: int


class R(BaseModel):
    x: float
    y: float


class Vector2(BaseModel):
    x: float
    y: float


class QParams(BaseModel):
    a: Optional[int] = None
    b: Optional[int] = None
    c: Optional[int] = None


# These are floats because ints can't handle large enough numbers
class Midpoint(BaseModel):
    a: float
    b: float
