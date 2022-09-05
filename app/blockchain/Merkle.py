import hashlib
import math

class Merkle:
    @staticmethod
    def to_bytes(combined_hash):
        x = [combined_hash[i:i + 2] for i in range(0, len(combined_hash), 2)]
        return [int(hex_, 16) for hex_ in x]

    @staticmethod
    def to_hex(bytes_):
        return ''.join('{:02x}'.format(x) for x in bytes_)

    @staticmethod
    def hash_pair(a, b=None):
        b = b if b else a
        bytes_ = Merkle.to_bytes(f'{b}{a}')[::-1]
        hashed = hashlib.sha256(bytes(bytes_)).hexdigest()
        hashed = hashlib.sha256(bytes(Merkle.to_bytes(hashed))).hexdigest()
        hashed = Merkle.to_bytes(hashed)
        return Merkle.to_hex(hashed[::-1])

    @staticmethod
    def to_pairs(arr):
        len_new_array = math.ceil(len(arr) / 2)
        new_array = [None] * len_new_array
        for i in range(len(new_array)):
            a = arr[i * 2: i * 2 + 2]
            new_array[i] = a
        return new_array

    @staticmethod
    def merkle_root(txs):
        if len(txs) == 1:
            return txs[0]
        else:
            to_pair = Merkle.to_pairs(txs)
            tree = []
            for pair in to_pair:
                tree.append(Merkle.hash_pair(pair[0], pair[1] if len(pair) == 2 else None))
            return Merkle.merkle_root(tree)

    @staticmethod
    def merkle_proof(txs, tx, proof=[]):
        if len(txs) == 1:
            return proof
        tree = []
        pairs = Merkle.to_pairs(txs)
        for pair in pairs:
            hash_ = Merkle.hash_pair(pair[0], pair[1] if len(pair) == 2 else None)
            if tx in pair:
                idx = 1 if pair[0] == tx else 0
                try:
                    proof.append([idx, pair[idx]])
                except:
                    proof.append([idx, None])
                tx = hash_
            tree.append(hash_)
        return Merkle.merkle_proof(tree, tx, proof)

    @staticmethod
    def merkle_proof_root(proof, tx):
        root = tx
        for p in proof:
            root = Merkle.hash_pair(root, p[1]) if p[0] else Merkle.hash_pair(p[1], root)
        return root

def main():
    t = [
        "5fb7f28bac287f888c976a6cf8085fb44ae7566d444628d9d9debdfbae8b313d",
        "6a555b78b00f38f8a12eb29b7d7be29bb98eb0cbdc1caaf69fbd0645f1239474",
        "8abc511c85bf8bc496e8e0e84b595c87f37fd8647c7aca06f25e2de4d501ac3f",
        "fa022ec86427f766b9767f124b98fe15b00216e1dd4fdc9270780bb958171fbf",
        "056907b33f71a108f4f4ac9e093a3ad29e6e9237aebc82d77f2cff6818230adc",
    ]
    import random
    import requests
    URL = "https://blockchain.info/rawblock/000000000000000000079b7da5cea599464404dbe339759919e00b48f15f8290?cors=true"
    r = requests.get(URL).json()
    oficial_merkle_root = r.get("mrkl_root")
    trans = r.get("tx")
    trans = [txt.get("hash") for txt in trans]
    recreated_merkle_root = Merkle.merkle_root(trans)

    if recreated_merkle_root == oficial_merkle_root:
        print("True")

    tx = random.choice(trans)
    print(tx)

    merkle_proof_ = Merkle.merkle_proof(trans, tx)
    print(merkle_proof_)
    if Merkle.merkle_proof_root(merkle_proof_,tx) == oficial_merkle_root:
        print("True")

if __name__ == "__main__":
    main()