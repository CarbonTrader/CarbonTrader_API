import hashlib
import math
import random

import requests

t = [
    "5fb7f28bac287f888c976a6cf8085fb44ae7566d444628d9d9debdfbae8b313d",
    "6a555b78b00f38f8a12eb29b7d7be29bb98eb0cbdc1caaf69fbd0645f1239474",
    "8abc511c85bf8bc496e8e0e84b595c87f37fd8647c7aca06f25e2de4d501ac3f",
    "fa022ec86427f766b9767f124b98fe15b00216e1dd4fdc9270780bb958171fbf",
    "056907b33f71a108f4f4ac9e093a3ad29e6e9237aebc82d77f2cff6818230adc",
]


def to_bytes(combined_hash):
    x = [combined_hash[i:i + 2] for i in range(0, len(combined_hash), 2)]
    return [int(hex_, 16) for hex_ in x]


def to_hex(bytes_):
    return ''.join('{:02x}'.format(x) for x in bytes_)


def hash_pair(a, b=None):
    b = b if b else a
    bytes_ = to_bytes(f'{b}{a}')[::-1]
    hashed = hashlib.sha256(bytes(bytes_)).hexdigest()
    hashed = hashlib.sha256(bytes(to_bytes(hashed))).hexdigest()
    hashed = to_bytes(hashed)
    return to_hex(hashed[::-1])


def to_pairs(arr):
    len_new_array = math.ceil(len(arr) / 2)
    new_array = [None] * len_new_array
    for i in range(len(new_array)):
        a = arr[i * 2: i * 2 + 2]
        new_array[i] = a
    return new_array


def merkle_root(txs):
    if len(txs) == 1:
        return txs[0]
    else:
        to_pair = to_pairs(txs)
        tree = []
        for pair in to_pair:
            tree.append(hash_pair(pair[0], pair[1] if len(pair) == 2 else None))
        return merkle_root(tree)


def merkle_proof(txs, tx, proof=[]):
    if len(txs) == 1:
        return proof
    tree = []
    pairs = to_pairs(txs)
    for pair in pairs:
        hash_ = hash_pair(pair[0], pair[1] if len(pair) == 2 else None)
        if tx in pair:
            print(pair)
            idx = 1 if pair[0] == tx else 0
            print(idx)
            try:
                proof.append([idx, pair[idx]])
            except:
                proof.append([idx, None])
            tx = hash_
        tree.append(hash_)
    return merkle_proof(tree, tx, proof)


def merkle_proof_root(proof, tx):
    root = tx
    for p in proof:
        root = hash_pair(root, p[1]) if p[0] else hash_pair(p[1], root)
    return root


URL = "https://blockchain.info/rawblock/000000000000000000079b7da5cea599464404dbe339759919e00b48f15f8290?cors=true"
r = requests.get(URL).json()
oficial_merkle_root = r.get("mrkl_root")
trans = r.get("tx")
trans = [txt.get("hash") for txt in trans]
recreated_merkle_root = merkle_root(trans)

if recreated_merkle_root == oficial_merkle_root:
    print("True")

tx = random.choice(trans)
print(tx)

merkle_proof_ = merkle_proof(trans, tx)
print(merkle_proof_)
print(oficial_merkle_root)
print(merkle_proof_root(merkle_proof_,tx))
"""
merkle_root_ = merkle_root(t)
print(merkle_root_)
tx = "fa022ec86427f766b9767f124b98fe15b00216e1dd4fdc9270780bb958171fbf"
merkle_proof_ =merkle_proof(t,tx)
print(merkle_proof_)
print(merkle_proof_root(merkle_proof_,tx))
"""