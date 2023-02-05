from typing import List
from hash_generator import HashGenerator

class CountMin():

    def __init__(self, D: int, K: int, N: int) -> None:
        """
        Initializes Count-Min Sketch class.

        Parameters
        ----------
        D: integer
            Size of input dimension.
        K: integer
            Number of buckets (width, prime number).
        N: integer
            Number of hash functions (height).

        """
        self.D = D
        self.K = K
        self.N = N

        self.hash_generators = [HashGenerator(self.K, self.D) for i in range(self.N)]
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