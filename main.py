from mtree import MerkleTree
from lap1 import LamportSignature

#algoritmul
#https://en.m.wikipedia.org/wiki/Merkle_signature_scheme



def main():

    N = 4  # nr de message

    # Generate 'N' private/public key pairs (Xi, Yi) from the Lamport signature scheme
    key_pairs = [LamportSignature() for _ in range(N)]  
    mk = MerkleTree(n_leaves=N)

    for i in range(N):
        mk.add_node(key_pairs[i].get_key('public', concatenate=True), (0, i), hashed=False)

    mk.generate_tree()
    pub = mk.get_root()  


    #Semnatura
    pair = 3  # (Xi, Yi) pair number
    sig = []
    M = "Dan Motpan"
    sig_prime = key_pairs[pair].sign(M)
    sig.append(sig_prime)  # Add sig_prime to the signature 'sig'.
    sig.append(key_pairs[pair].get_key('public', concatenate=True))  # Add Yi to the signature 'sig'.
  

    # Verificarea
    # Receiver knows the public key 'pub' (tree root), the message 'M' and the Merkle signature 'sig'.
    pub_receiver = pub
    M_receiver = M
    sig_receiver = sig

    # First, the receiver verifies the one time signature 'sig_prime' of the message 'M' using the Lamport key 'Yi'.
    print("Check one time signature of the received message: " + M_receiver)
    result = LamportSignature.verify(M_receiver, sig_receiver[0], LamportSignature.decatenate_key(sig_receiver[1]))
    print("One-time signature is: " + str(result))

    # If 'sig_prime' is a valid signature of 'M', the receiver computes the leaf corresponding to the Lamport key 'Yi'.
    if result:
        mk_receiver = MerkleTree(n_leaves=N)
        mk_receiver.add_node(sig_receiver[1], (0, pair), hashed=False)
        mk_receiver.generate_tree()

    #
    #                       NOTE
    #  Verificarea semnaturii nu este finalizata
    #  Este necesar de verificat positia nodurilor vecine ,si lista indexilor.
        
if __name__ == "__main__":
    main()