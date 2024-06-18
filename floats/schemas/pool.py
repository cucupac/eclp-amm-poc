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

class AMMParams(BaseModel):
    input: float
    translated_reserve_out: float
    λ_sq: float
    input_scale: float
    rate_out: float
    pc1: float
    pc2: float
    pc3: float
    pc4: float
    pc5: float