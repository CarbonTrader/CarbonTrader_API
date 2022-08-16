from app.services.CryptoHash import CryptoHash
import time

class Transaction:

    def __init__(self, id, transaction_type, carbon_trader_serial, seller, buyer):
        self.id = id
        self.timestamp = time.time_ns()
        self.buyer = buyer
        self.seller = seller
        self.carbon_trader_serial = carbon_trader_serial
        self.transaction_type = transaction_type
        self.hash = None

    def generate_hash(self):
        return  CryptoHash.get_hash(self.id,self.buyer,self.seller,self.carbon_trader_serial,self.transaction_type,self.timestamp)

    def __repr__(self):
        return (
            'Transaction('
            f'_id: {self.id}, '
            f'timestamp: {self.timestamp}, '
            f'hash: {self.hash}, '
            f'seller: {self.seller},'
            f'carbon_trader_serial: {self.carbon_trader_serial},'
            f'transaction_type: {self.transaction_type}),'
        )

def main():
    t = Transaction("1","2","123","yp","tu")
    print(t.generate_hash())


if __name__ == '__main__':
    main()

