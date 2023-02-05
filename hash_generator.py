import random
from typing import List

class HashGenerator():

    def __init__(self, p: int, k: int) -> None:
        """ 
        Initializes Hash class.

        Parameters
        ----------
        p: integer
            Choose a primer integer p such that p >= n,
            where n is the range of possible inputs in universe.
            (e.g. for ASCII: p >= 128)

        k: integer
            Output dimension. For strings, this would be the max
            input string length. Shorter strings are padded.

        """
        self.p = p
        self.k = k

    def generate_hash_function(self) -> List[int]:
        """
        Generates hash function as follows:
            select k integers {z1, ..., zk} by U.A.R. sampling 
            k times from the set {0, ..., p - 1}

        """
        self.z = [random.randint(0, self.p - 1) for i in range(self.k)]
        return self.z

    def hash(self, s: str) -> int:
        """
        Hashes input string as follows:
        h(a1, ..., ak) = (SUM_overall_zs zi * ai) mod p

        Parameters
        ----------
        s: string
            Input string to be hashed.

        """
        s = s.ljust(self.k, " ")
        emb = [ord(ch) for ch in s]

        return sum(map(lambda x: x[0] * x[1], zip(self.z, emb[:self.k]))) % self.p