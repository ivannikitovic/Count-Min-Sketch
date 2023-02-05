from math import sqrt
import random
from typing import List

class HashGenerator():

    def __init__(self, n: int, k:int, m: int, p: int = None) -> None:
        """ 
        Initializes Hash class.

        Parameters
        ----------
        n: integer
            Input range.
            (e.g. for ASCII: n == 128)
        
        k: integer
            Input length. For strings, this would be the max
            input string length. Shorter strings are padded.

        m: integer
            Output dimension.
            ([n] -> [m])

        p: integer, optional
            Prime number such that p > n > m.

        """
        self.n = n
        self.k = k
        self.m = m
        self.p = p

        if not self.p:
            self.find_prime()

    def find_prime(self) -> None:
        """
        Starting from self.n, find the next larger prime number.

        """
        curr = self.n
        while not self.p:
            upper = int(sqrt(curr))
            for i in range(2, upper + 1):
                if curr % i == 0:
                    break
                if i == upper:
                    self.p = curr
            
            curr += 1

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

        z_a = sum(map(lambda x: x[0] * x[1], zip(self.z, emb[:self.k])))

        return  (z_a % self.p) % self.m