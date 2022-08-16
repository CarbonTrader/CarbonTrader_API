from app.Model.Wallet import Wallet
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature

class WalletService:
    @staticmethod
    def sign(wallet: Wallet, data):
        """
        Generate signature based on the data using the local private key.
        """
        return wallet.private_key.sign(json.dumps(data).encode('utf-8'), ec.ECDSA(hashes.SHA256()))

    @staticmethod
    def verify(public_key, data, signature):
        """
        Verify a signature based on the orginal public key and data.
        """
        try:
            public_key.verify(signature, json.dumps(data).encode('utf-8'), ec.ECDSA(hashes.SHA256()))
            return True
        except InvalidSignature:
            return False

    @staticmethod
    def test():
        wallet = Wallet()
        print(f'wallet.__dict__: {wallet.__dict__}')
        data = {'foo': 'bar'}
        signature = WalletService.sign(wallet,data)
        print(f'signature: {signature}')

        should_be_valid = WalletService.verify(wallet.public_key, data, signature)
        print(f'should_be_valid: {should_be_valid}')

        should_be_invalid = WalletService.verify(Wallet().public_key, data, signature)
        print(f'should_be_invalid: {should_be_invalid}')