from app.Model.Block import Block
from app.services.CryptoHash import CryptoHash

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
        transaction_hashes.append(transaction_hashes[-1]) if len(transaction_hashes) % 2 != 0 else transaction_hashes

    @staticmethod
    def mine_block(last_block: Block, transactions):
        """
        Mine a block based on the given last_block and data.
        """
        new_block = Block(last_block.hash)
        new_block.number_transactions = len(transactions)
        new_block.transactions_hashes = transactions[:]
        new_block.merkle_root = Block.get_merkle_root(transactions[:])
        new_block.hash = CryptoHash.get_hash(new_block.timestamp, new_block.last_hash, new_block.merkle_root,
                                             new_block.number_transactions, new_block.transactions_hashes)

        with open("new_block.json", "w") as outfile:
            outfile.write(json.dumps(new_block.__dict__, sort_keys=True, indent=4, separators=(',', ': ')))

        return new_block

    @staticmethod
    def test():

        pass
