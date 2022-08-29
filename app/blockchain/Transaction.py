import time

from CryptoHash import CryptoHash
from Wallet import Wallet


class Transaction:

    def __init__(self, id, transaction_type, carbon_trader_serial, sender_wallet: Wallet, recipient):
        self.id = id
        self.timestamp = time.time_ns()
        self.recipient_address = recipient
        self.sender_address = sender_wallet.address
        self.carbon_trader_serial = carbon_trader_serial
        self.transaction_type = transaction_type
        self.public_key = sender_wallet.public_key
        self.hash = self.generate_hash()
        self.signature = sender_wallet.sign(self.__dict__)

    def generate_hash(self):
        return CryptoHash.get_hash(self.id, self.timestamp, self.recipient_address, self.sender_address,
                                   self.carbon_trader_serial,
                                   self.transaction_type, self.public_key)




def main():
    wallet = Wallet()
    print(wallet.__dict__)
    trans = Transaction("id", "type", "serial", wallet, "recipient")
    print(trans.__dict__)

if __name__ == '__main__':
    main()
