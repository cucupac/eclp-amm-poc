import os
import sys
from decimal import Decimal

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schemas.vault import VaultTokenInfo, TokenBalances


def get_token_balances(tokens: VaultTokenInfo) -> TokenBalances:

    return TokenBalances(
        x_0=tokens.x_0.amount / (10**tokens.x_0.decimals),
        y_0=tokens.y_0.amount / (10**tokens.y_0.decimals),
    )
