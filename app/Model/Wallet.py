import uuid
from pydantic import BaseModel
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec


class Wallet:
    """
    An Individual wallet for a miner.
    Keeps track of the mine's balance.
    Allows a miner to authorizse transactions
    """
    # TODO: Invesigar
    def __init__(self):
        self.address = str(uuid.uuid4())[0:8]
        self.private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
        self.public_key = self.private_key.public_key()
        self.my_credits = []
