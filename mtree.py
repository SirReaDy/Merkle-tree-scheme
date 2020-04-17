import hashlib
from math import log2, floor

class MerkleTree:

    def __init__(self, n_leaves):
        self.tree = {}
        self.n_levels = None
        self.n_leaves = n_leaves

    @staticmethod
    def hash(data):

        if type(data) is not bytearray:
            data = data.encode('utf-8')
        return bytearray(hashlib.sha256(data).digest())

    def add_node(self, data, position, hashed=False):
    
        if data is None:
            self.tree[position] = None
        elif hashed and type(data) is str:
            self.tree[position] = bytearray.fromhex(data)
        elif hashed and type(data) is bytearray:
            self.tree[position] = data
        else:
            self.tree[position] = self.hash(data)

    def double_hash(self,hash_string):
        first_hash = hashlib.sha256(hash_string.encode()).hexdigest()
        return hashlib.sha256(first_hash.encode()).hexdigest()


    def get_root(self):

        return self.tree[(self.n_levels - 1, 0)]

    def turn_into_hash(self,hash_list):  # In caz ca avem nevoie de hashare
        hashed_hashlist = []
        for item in hash_list:
            item = self.double_hash(item)
            hashed_hashlist.append(item)
        return hashed_hashlist



    def generate_tree(self):

        self.n_levels = int(log2(self.n_leaves)) + 1
        for level in range(self.n_levels):
            for pos in range(int(self.n_leaves / 2 ** level)):
                if (level, pos) not in self.tree:
                    self.tree[(level, pos)] = None

        for level in range(1, self.n_levels):
            for pos in range(int(self.n_leaves / 2 ** level)):
                left_child = self.tree[(level - 1, 2 * pos)]
                right_child = self.tree[(level - 1, 2 * pos + 1)]
                if left_child is not None and right_child is not None:
                    self.tree[(level, pos)] = self.hash(left_child + right_child)


'''
#     
#metoda pentru afisarea hasului a unei liste
#     
    def create_tree(self,hash_list):
            child_hash_list = []
            # Incepem cu primu el,si le grupam cate 2
            for index in range(0, len(hash_list)-1, 2):

                # Dacalungimea el nu este 64, hasham cu sha256
                if len(list(hash_list[index])) != 64:
                    hash_list = self.turn_into_hash(hash_list)

                left = hash_list[index]
                right = hash_list[index + 1] # concatinarea ambele nodurilor

                child_hash_list.append(self.double_hash(left + right))  # Gruparea hashelor

            if len(hash_list) % 2 == 1:  # Dacă este un nr impar deele în lista,hasham ultimul el cu el insuti
                child_hash_list.append(hash_list[-1])  # Append the last element 


            if len(hash_list) == 1:  # Dacă s-a ajuns la radacina , finalizam si i returm hash-ul radacina
                print("Merkle root:")
                return hash_list[0]

            return self.create_tree(child_hash_list)  #Apelam Recursiv pana cand  lungimea listei hash este 1
'''


'''
if __name__ == "__main__":

        example_hash_list = [
            "aa",
            "bb",
            "cc"
            ]
        print(create_tree(example_hash_list))
'''