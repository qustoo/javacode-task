import uuid
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, condecimal

WalletID = Annotated[
    uuid.UUID,
    Field(
        ...,
        default_factory=uuid.uuid4,
        description="Уникальный идентификатор кошелька, присвоенный сервером",
    ),
]


class Transaction(BaseModel):
    amount: condecimal(ge=0, allow_inf_nan=False)


class WalletResponse(BaseModel):
    id: WalletID
    balance: Decimal
    model_config = ConfigDict(from_attributes=True)
