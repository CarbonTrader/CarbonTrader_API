from app.services.CryptoHash import CryptoHash


S = [
    "416dc4c02b98dbdea5cb0b055fc25883829f9ff9a2eb35423700b6cf37dc782a",
    "eb418b77a914ff1e8d4ff30b61b958ae504ea00e98086e50756e474d3fa1d43a",
    "a1d6d009b65a313c9db3cf2d65b34f913ba53ab7a27ef11b5aa8b30bc672bf75"
    ]
def get_merkle_root(transactions):
    aux = []
    complete_list(transactions)
    while len(transactions) != 0:
        first ,second = transactions[0], transactions[1]
        transactions = transactions[2:]
        aux.append(CryptoHash.get_hash(first,second))
        if len(transactions) == 0 and len(aux) > 1:
            transactions = aux[:]
            aux = []
            complete_list(transactions)


    return aux[0]

def complete_list(transactions):
    transactions.append(transactions[-1]) if len(transactions) % 2 != 0 else transactions


print(S)
print(get_merkle_root(S))
print(len(get_merkle_root(S)))

