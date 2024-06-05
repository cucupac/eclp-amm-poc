from pydantic import BaseModel

from floats.schemas.token import Token


class VaultTokenInfo(BaseModel):
    x_0: Token
    y_0: Token


class TokenBalances(BaseModel):
    x_0: float
    y_0: float
