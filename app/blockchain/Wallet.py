import json
import uuid

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.utils import (
encode_dss_signature, decode_dss_signature
)
from cryptography.hazmat.primitives.asymmetric import ec


class Wallet:
    """
    An Individual wallet for a miner.
    Keeps track of the mine's balance.
    Allows a miner to authorizse transactions
    """

    def __init__(self):
        self.address = str(uuid.uuid4())
        self.private_key = None
        self.generate_private_key()
        self.public_key = None
        self.generate_public_key()
        self.my_credits = []

    def upload_wallet(self, address=None, private_key= None, public_key = None, my_credits = []):
        self.address = address
        self.private_key = private_key
        self.public_key = public_key
        self.my_credits = my_credits

    def generate_public_key(self):
        self.deserialize_private_key()
        self.public_key = self.private_key.public_key()
        self.serialize_private_key()
        self.serialize_public_key()

    def generate_private_key(self):
        self.private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
        self.serialize_private_key()

    def sign(self, transaction):
        """
        Generate signature based on the data using the local private key.
        """
        self.deserialize_private_key()
        signature = self.private_key.sign(json.dumps(transaction).encode('utf-8'), ec.ECDSA(hashes.SHA256()))
        self.serialize_private_key()
        return decode_dss_signature(signature)

    @staticmethod
    def verify(ser_public_key, transaction, signature):
        """
        Verify a signature based on the orginal public key and data.
        """
        (r,s) = signature
        try:
            ser_public_key.verify(encode_dss_signature(r,s), json.dumps(transaction).encode('utf-8'), ec.ECDSA(hashes.SHA256()))
            return True
        except InvalidSignature:
            return False

    def serialize_public_key(self):
        """
        Reset the public key to its serialized version.
        """
        if type(self.public_key) != str:
            self.public_key = self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo).decode('utf-8')

    def deserialize_public_key(self):
        if type(self.public_key) == str:
            self.public_key = serialization.load_pem_public_key(self.public_key.encode('utf-8'), default_backend())

    def serialize_private_key(self):
        if type(self.private_key) != str:
            self.private_key = self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ).decode('utf-8')

    def deserialize_private_key(self):
        if type(self.private_key) == str:
            self.private_key = serialization.load_pem_private_key(self.private_key.encode('utf-8'), None,
                                                                  default_backend())



def test():
    wallet = Wallet()
    print(f'wallet.__dict__: {wallet.__dict__}')
    data = {'foo': 'bar'}
    signature = Wallet.sign(wallet, data)
    print(f'signature: {signature}')

    wallet.deserialize_public_key()
    should_be_valid = Wallet.verify(wallet.public_key, data, signature)

    print(f'should_be_valid: {should_be_valid}')
    wallet.deserialize_public_key()
    print(wallet.public_key)
    wallet.serialize_public_key()
    print(wallet.public_key)
    print("-------------------------------------------------------")
    print(wallet.private_key)
    wallet.deserialize_private_key()
    print(wallet.private_key)

if __name__ == "__main__":
    test()
