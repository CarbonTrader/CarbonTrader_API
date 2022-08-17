from app.Model.Block import Block
from app.services.CryptoHash import CryptoHash
import json

GENESIS_LAST_HASH = "0000000000000000000000000000000000000000000000000000000000000000"


class BlockService:
    @staticmethod
    def get_merkle_root(transaction_hashes):
        aux = []
        BlockService.complete_list(transaction_hashes)
        while len(transaction_hashes) != 0:
            first, second = transaction_hashes[0], transaction_hashes[1]
            transaction_hashes = transaction_hashes[2:]
            aux.append(CryptoHash.get_hash(first, second))
            if len(transaction_hashes) == 0 and len(aux) > 1:
                transaction_hashes = aux[:]
                aux = []
                BlockService.complete_list(transaction_hashes)

        return aux[0]

    @staticmethod
    def complete_list(transaction_hashes):
        transaction_hashes.append(
            transaction_hashes[-1]) if len(transaction_hashes) % 2 != 0 else transaction_hashes

    # TODO: Transaction create hashes
    @staticmethod
    def mine_block(last_block: Block, transactions):
        """
        Mine a block based on the given last_block and data.
        """
        new_block = Block(last_hash=last_block.hash)
        new_block.number_transactions = len(transactions)
        new_block.transactions_hashes = transactions[:]
        new_block.merkle_root = BlockService.get_merkle_root(transactions[:])
        new_block.hash = CryptoHash.get_hash(new_block.timestamp, new_block.last_hash, new_block.merkle_root,
                                             new_block.number_transactions, new_block.transactions_hashes)

        with open("new_block.json", "w") as outfile:
            outfile.write(json.dumps(new_block.__dict__,
                          sort_keys=True, indent=4, separators=(',', ': ')))

        return new_block

    @staticmethod
    def genesis():
        """
        Generate the genesis block.
        """
        genesis_block = Block(last_hash=GENESIS_LAST_HASH)
        genesis_block.hash = CryptoHash.get_hash(genesis_block.timestamp, genesis_block.last_hash,
                                                 genesis_block.merkle_root, genesis_block.number_transactions,
                                                 genesis_block.transactions_hashes)
        return genesis_block

    @staticmethod
    def test():
        genesis = BlockService.genesis()
        BlockService.mine_block(genesis, ["1", "2", "3", "4"])
        pass
