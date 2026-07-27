from decimal import Decimal

from pydantic import BaseModel


class MessageResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    detail: str


class MoneyRequest(BaseModel):
    amount: Decimal
    currency: str = "USD"


class MoneyResponse(BaseModel):
    amount: Decimal
    currency: str
