import json
import time

from CryptoHash import CryptoHash

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
    def get_merkle_root(transactions):
        aux = []
        Block.complete_list(transactions)
        while len(transactions) != 0:
            first, second = transactions[0], transactions[1]
            transactions = transactions[2:]
            aux.append(CryptoHash.get_hash(first, second))
            if len(transactions) == 0 and len(aux) > 1:
                transactions = aux[:]
                aux = []
                Block.complete_list(transactions)

        return aux[0]

    @staticmethod
    def complete_list(transactions):
        transactions.append(transactions[-1]) if len(transactions) % 2 != 0 else transactions

    @staticmethod
    def mine_block(last_block, transactions):
        """
        Mine a block based on the given last_block and data.
        """
        new_block = Block(last_block.hash)
        new_block.number_transactions = len(transactions)
        new_block.transactions_hashes = transactions[:]
        new_block.hash = CryptoHash.get_hash(new_block.timestamp, new_block.last_hash, new_block.merkle_root,
                                             new_block.number_transactions, new_block.transactions_hashes)
        new_block.merkle_root = Block.get_merkle_root(transactions[:])
        with open("new_block.json", "w") as outfile:
            outfile.write(json.dumps(new_block.__dict__, sort_keys=True, indent=4, separators=(',', ': ')))

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
    def is_valid_block(last_block, block):
        """
        Validate a block by enforcing the following rules:
        - The block must have the proper last_hash reference
        - The block must meet the consensus algo requirement
        - The block hash must be a vallid convination of the block fields
        """

        if block.last_hash != last_block.hash:
            raise Exception('The block last_hash must be correct.')

        reconstructed_hash = CryptoHash.get_hash(
            block.timestamp,
            block.last_hash,
            block.hash,
            block.data,

        )


def main():
    genesis_block = Block.genesis()
    block = Block.mine_block(genesis_block, 'foo')
    print(f'block: {block}')


if __name__ == '__main__':
    main()
