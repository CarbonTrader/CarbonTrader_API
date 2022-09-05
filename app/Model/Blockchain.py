import time
from typing import Union, List

from pydantic import BaseModel

from .Block import Block

from ..services.BlockService import BlockService


class Blockchain(BaseModel):
    chain: List[Block] = [BlockService.genesis()]
