from Block import Block
from Transaction import Transaction
from types import SimpleNamespace
import json

from Wallet import Wallet


class Blockchain:
    """
    Blockchain: a public ledger of transactions.
    Implemented as a list of blocks - data sets of transactions
    """

    def __init__(self):
        self.chain = [Block.genesis()]

    def create_not_verify_block(self, transactions):
        return Block.mine_block(self.chain[-1], transactions)
    def add_block(self, new_block):
        self.chain.append(new_block)

    def __repr__(self):
        return f'Blockchain: {self.chain}'

    def update_chain_file(self):
        with open("blockchain.json", "w") as outfile:
            outfile.write(json.dumps([block.__dict__ for block in self.chain], sort_keys=False, indent=4, separators=(',', ': ')))

    @staticmethod
    def update_local_transactions(new_transaction):
        transactions = []
        try:
            with open('local_transactions.json') as f:
                transactions = json.load(f)
        except:
            print("There was a problem fetching local_transactions.json")

        transactions.append(new_transaction.__dict__)
        try:
            with open("local_transactions.json", "w") as outfile:
                outfile.write(
                    json.dumps([transaction for transaction in transactions], sort_keys=False, indent=4, separators=(',', ': ')))
        except Exception as e:
            print(e)
            print("There was a problem writting local_transactions.json")

    @staticmethod
    def reset_local_transactions():
        transactions = []
        try:
            with open("local_transactions.json", "w") as outfile:
                outfile.write(
                    json.dumps([transaction for transaction in transactions], sort_keys=False, indent=4,
                               separators=(',', ': ')))
        except Exception as e:
            print(e)
            print("There was a problem writting local_transactions.json")


    @staticmethod
    def fetch_transactions():
        try:
            with open('local_transactions.json') as f:
                transactions = json.load(f)
                return transactions
        except:
            print("There was a problem fetching local_transactions.json")
            return None

    @staticmethod
    def obtain_transactions_hashes(transactions):
        return [transaction.get("hash") for transaction in transactions]
def main():
    Blockchain.reset_local_transactions()
    blockchain = Blockchain()
    wallet_1 = Wallet()
    wallet_2 = Wallet()
    trans = Transaction("id","type","serial",wallet_1,"recipient")
    trans2 = Transaction("id2","type","serial",wallet_2,"recipient")
    trans3 = Transaction("id3","type","serial",wallet_1,"recipient")
    trans4 = Transaction("id4","type","serial",wallet_2,"recipient")
    trans5 = Transaction("id5","type","serial",wallet_2,"recipient")
    Blockchain.update_local_transactions(trans)
    Blockchain.update_local_transactions(trans2)
    Blockchain.update_local_transactions(trans3)
    Blockchain.update_local_transactions(trans4)
    Blockchain.update_local_transactions(trans5)
    transactions = Blockchain.fetch_transactions()
    transactions_hashes = Blockchain.obtain_transactions_hashes(transactions)
    new_block = blockchain.create_not_verify_block(transactions_hashes)
    block_from_file = Block.fetch_new_block()
    if Block.is_valid_block(block_from_file,blockchain.chain[-1],transactions, transactions_hashes):
        print("Block is valid")
        blockchain.add_block(new_block)
    blockchain.update_chain_file()


if __name__ == '__main__':
    main()
