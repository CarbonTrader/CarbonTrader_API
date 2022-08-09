from Block import Block
from Transaction import Transaction

import json

class Blockchain:
    """
    Blockchain: a public ledger of transactions.
    Implemented as a list of blocks - data sets of transactions
    """

    def __init__(self):
        self.chain = [Block.genesis()]

    def add_block(self, transactions):
        self.chain.append(Block.mine_block(self.chain[-1], transactions))

    def __repr__(self):
        return f'Blockchain: {self.chain}'

    @staticmethod
    def update_chain_file(chain):
        with open("blockchain.json", "w") as outfile:
            outfile.write(json.dumps([block.__dict__ for block in chain], sort_keys=True, indent=4, separators=(',', ': ')))


def main():
    blockchain = Blockchain()
    transaction1 = Transaction("1","commerce","123456","user1","user2")
    transaction2 = Transaction("2","commerce","123456","user2","user1")
    transaction3 = Transaction("3","retire","123456","user2","anon")
    transaction4 = Transaction("4","retire","123456","user1","anon")
    transaction5 = Transaction("5","retire","1234567","user3","anon")

    blockchain.add_block([transaction1.generate_hash(),transaction2.generate_hash(),transaction5.generate_hash()])
    blockchain.add_block([transaction3.generate_hash(), transaction4.generate_hash()])
    blockchain.update_chain_file(blockchain.chain)
    transactions = []
    while True:
        res = input("Welcome, wold you like to make a transaction? (y/n): ")
        print(res)
        if res != 'y':
            exit()
        _id = input("Transaction id: ")
        buyer = input("Buyer: ")
        seller = input("Seller: ")
        carbon_trader_serial = input("Carbon_trader_serial: ")
        transaction_type = input("Transaction_type: ")
        transaction = Transaction(id,transaction_type,carbon_trader_serial,buyer,seller)
        transactions.append(transaction)
        if len(transactions) == 2:
            print("Block closed!")
            blockchain.add_block([trans.generate_hash() for trans in transactions])
            blockchain.update_chain_file(blockchain.chain)
            transactions = []

if __name__ == '__main__':
    main()