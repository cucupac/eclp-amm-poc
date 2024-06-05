from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    address: str
    amount: float
    decimals: Optional[int] = None
