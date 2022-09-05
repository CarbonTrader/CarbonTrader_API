import json
import time

from CryptoHash import CryptoHash
from Wallet import Wallet
from Merkle import Merkle

GENESIS_LAST_HASH = "0000000000000000000000000000000000000000000000000000000000000000"


class Block:
    """
    Block: a unit of storage.
    Store transactions in a blockchain that supports a cryptocurrency.
    """

    def __init__(self, last_hash):
        self.timestamp = time.time_ns()
        self.last_hash = last_hash
        self.hash = None
        self.merkle_root = None
        self.number_transactions = 0
        self.transactions_hashes = []

    def __repr__(self):
        return (
            'Block('
            f'timestamp: {self.timestamp}, '
            f'last_hash: {self.last_hash}, '
            f'hash: {self.hash}, '
            f'transactions: {self.transactions_hashes}),'
            f'merkle_root: {self.merkle_root},'
            f'number of transactions: {self.number_transactions},'
            f'transactions: {self.transactions_hashes})'
        )


    @staticmethod
    def mine_block(last_block, transactions_hashes):
        """
        Mine a block based on the given last_block and data.
        """
        new_block = Block(last_block.hash)
        new_block.number_transactions = len(transactions_hashes)
        new_block.transactions_hashes = transactions_hashes[:]
        new_block.merkle_root = Merkle.merkle_root(transactions_hashes[:])
        new_block.hash = CryptoHash.get_hash(new_block.timestamp, new_block.last_hash, new_block.merkle_root,
                                             new_block.number_transactions, new_block.transactions_hashes)

        with open("new_block.json", "w") as outfile:
            outfile.write(json.dumps(new_block.__dict__, sort_keys=False, indent=4, separators=(',', ': ')))

        return new_block

    @staticmethod
    def genesis():
        """
        Generate the genesis block.
        """
        genesis_block = Block(GENESIS_LAST_HASH)
        genesis_block.hash = CryptoHash.get_hash(genesis_block.timestamp, genesis_block.last_hash,
                                                 genesis_block.merkle_root, genesis_block.number_transactions,
                                                 genesis_block.transactions_hashes)
        return genesis_block

    @staticmethod
    def fetch_new_block():
        try:
            with open('new_block.json') as f:
                block = json.load(f)
                return block
        except:
            print("There was a problem fetching new_block.json")
            return None

    @staticmethod
    def is_valid_block(new_block, last_block, transactions, transactions_hashes):

        for transaction in transactions:
            if not Block.is_valid_signature(transaction.get("public_key"), transaction, transaction.get("signature")):
                print(f'The transaction {transaction.get("id")} is not valid.')
                return False

        reconstructed_merkle = Merkle.merkle_root(transactions_hashes[:])
        if reconstructed_merkle != new_block.get("merkle_root"):
            print('The merkle root is not valid.')
            return False

        if new_block.get("last_hash") != last_block.hash:
            print('The block last_hash is not valid.')
            return False

        reconstructed_hash = CryptoHash.get_hash(new_block.get("timestamp"), new_block.get("last_hash"),
                                                 new_block.get("merkle_root"),
                                                 new_block.get("number_transactions"),
                                                 new_block.get("transactions_hashes"))
        if new_block.get("hash") != reconstructed_hash:
            print('The block hash is not valid.')
            return False

        return True

    @staticmethod
    def is_valid_signature(public_key, transaction, signature):
        signature = (signature[0], signature[1])
        del transaction["signature"]
        wallet = Wallet()
        wallet.upload_wallet(public_key=public_key)
        wallet.deserialize_public_key()
        return Wallet.verify(wallet.public_key, transaction, signature)


def main():
    genesis_block = Block.genesis()
    block = Block.mine_block(genesis_block, 'foo')
    print(f'block: {block}')


if __name__ == '__main__':
    main()
