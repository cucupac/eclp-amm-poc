from pydantic import BaseModel

"""FLOATS"""


class Params(BaseModel):
    alpha: float
    beta: float
    c: float
    s: float
    λ: float


class DerivedParams(BaseModel):
    tau_alpha_x: float
    tau_alpha_y: float
    tau_beta_x: float
    tau_beta_y: float
    u: float
    v: float
    w: float
    z: float
    d_sq: float


class R(BaseModel):
    x: float
    y: float


class Midpoint(BaseModel):
    a: float
    b: float


class Vector2(BaseModel):
    x: float
    y: float


class RateProviders(BaseModel):
    rate_provider_0: str
    rate_provider_1: str
