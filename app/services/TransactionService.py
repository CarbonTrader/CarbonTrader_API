from app.Model.Transaction import Transaction
from app.blockchain.CryptoHash import CryptoHash


class TransactionService:
    @staticmethod
    def generate_hash(transaction: Transaction):
        return CryptoHash.get_hash(transaction.id, transaction.recipient, transaction.sender_wallet,
                                   transaction.carbon_trader_serial, transaction.transaction_type,
                                   transaction.timestamp)

    @staticmethod
    def test():
        t = Transaction(sender_wallet="1", recipient="2", carbon_trader_serial="123", transaction_type="yp")
        print(TransactionService.generate_hash(t))
