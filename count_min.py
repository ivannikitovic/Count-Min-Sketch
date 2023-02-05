from typing import List
from hash_generator import HashGenerator

class CountMin():

    def __init__(self, K: int, N: int, i_dim: int = 128, i_len: int = 32) -> None:
        """
        Initializes Count-Min Sketch class.

        Parameters
        ----------
        K: integer
            Number of buckets (width, prime number).

        N: integer
            Number of hash functions (height).

        i_dim: integer, optional
            Input range.
            (e.g. for ASCII: n == 128)

        i_len: integer, optional
            Input length.

        """
        self.K = K
        self.N = N

        self.i_dim = i_dim
        self.i_len = i_len

        self.hash_generators = [HashGenerator(self.i_dim, self.i_len, self.K) for i in range(self.N)]
        for hg in self.hash_generators:
            hg.generate_hash_function()
        
        self.sketch = [[0 for i in range(self.K)] for j in range(self.N)]

    def process_stream(self, stream: List[object]) -> None:
        """
        Executes the CMS algorithm on a stream (list) of elements.

        Parameters
        ----------
        stream: List[object]
            Stream of objects represented as a list.

        """
        for value in stream:
            for i in range(self.N):
                bucket = self.hash_generators[i].hash(value)
                self.sketch[i][bucket] += 1

    def get_freq(self, values: List[object]) -> List[int]:
        """
        Returns the frequencies of elements in the CMS.

        Parameters
        ----------
        values: List[object]
            List of elements for which to return frequencies.

        """
        l = len(values)
        self.frequencies = {}

        for val_idx in range(l):
            if values[val_idx] not in self.frequencies:
                self.frequencies[values[val_idx]] = \
                min([self.sketch[i][self.hash_generators[i].hash(values[val_idx])] \
                      for i in range(self.N)])

        return self.frequencies