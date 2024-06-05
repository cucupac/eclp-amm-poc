from pydantic import BaseModel


class Rates(BaseModel):
    rate_0: float
    rate_1: float
