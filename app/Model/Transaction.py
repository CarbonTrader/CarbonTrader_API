import time
import uuid
from typing import Union

from pydantic import BaseModel


class Transaction(BaseModel):
    id: str = str(uuid.uuid4())
    timestamp: int = time.time_ns()
    sender_wallet: Union[str, None]
    recipient: Union[str, None]
    carbon_trader_serial: Union[str, None]
    transaction_type: Union[str, None]
    hash: Union[str, None] = None
