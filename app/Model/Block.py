import time
from typing import Union, List

from pydantic import BaseModel


class Block(BaseModel):
    """
    Block: a unit of storage.
    Store transactions in a blockchain that supports a cryptocurrency.
    """
    timestamp: int = time.time_ns()
    last_hash: str
    hash: Union[str, None] = None
    merkle_root: Union[str, None] = None
    number_transactions: Union[int, None] = 0
    transactions_hashes: Union[List[str], None] = []
