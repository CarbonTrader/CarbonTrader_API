import hashlib
import json


class CryptoHash:
    """
    Return a sha-256 hash of the given arguments.
    """
    @staticmethod
    def get_hash(self, *args):
        stringify_args = sorted(map(lambda data: json.dumps(data), args))
        joined_data = ''.join(stringify_args)
        return hashlib.sha256(joined_data.encode('utf-8')).hexdigest()


def main():
    print(f"crypto_hash('one', 2, [3]): {CryptoHash.get_hash('one', 2, [3])}")
    print(f"crypto_hash(2, 'one', [3]): {CryptoHash.get_hash(2, 'one', [3])}")


if __name__ == '__main__':
    main()
