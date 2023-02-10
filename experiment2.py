from math import ceil
import math
import re
from matplotlib import pyplot as plt
from count_min_sketch import CountMinSketch

# Experiment 2 (Shakespeare)

class CMS_Text():

    def __init__(self, epsilon: float, delta: float, path: str) -> None:
        """
        Initializes CMS Text class.

        Parameters
        ----------
        epsilon: float
            Epsilon from the epsilon-delta definition of the CMS.

        delta: float
            Delta from the epsilon-delta definition of the CMS.

        path: string
            Filepath to text file.

        """
        self.epsilon = epsilon
        self.delta = delta
        self.path = path


    def import_text(self, path: str):
        """
        Import text file from filepath.

        Parameters
        ----------
        path: string
            Filepath to text file.

        Returns
        -------
        corpus: list[str]
            List of strings containing cleaned input text.
        
        actual_freq: dict
            Dictionairy mapping frequencies to words in corpus.
            
        """
        with open(path, 'r') as file:
            raw = file.read().replace('\n', ' ')
            corpus = re.sub(r'[^A-Za-z0-9 ]+', '', raw).lower().split()

        actual_freq = {}

        for word in corpus:
            if word not in actual_freq:
                actual_freq[word] = 1
            else:
                actual_freq[word] += 1

        return corpus, actual_freq
    
    def compute_error(self, est_freq: dict, actual_freq: dict) -> dict:
        """
        Computes the absolute error between word frequency counts.

        Parameters
        ----------
        est_freq: dict
            Our estimated frequency from CMS.

        actual_freq: dict
            Actual frequency not seen by CMS.

        """
        error_freq = {}

        for word in actual_freq:
            diff = est_freq[word] - actual_freq[word]
            if diff not in error_freq:
                error_freq[diff] = 1
            else:
                error_freq[diff] += 1

        return error_freq
    
    def run_and_plot(self):
        """
        Runs the CMS on the text input and plots a graph that depicts
        the observed frequency of overestimating by a given amount.

        """
        corpus, actual_freq = self.import_text(self.path)
        N = sum(actual_freq.values())

        print(f"Number of unique words: {len(actual_freq)}")
        print(f"Number of words, total: {N}")
        print()

        w = ceil(math.e / self.epsilon) # 272 when epsilon == 0.01
        print(f"width: {w}")

        h = ceil(math.log(1 / self.delta)) # 3 when delta = 0.05
        print(f"height: {h}")

        print()

        # estimate less than epsilon * N with probability 1 - delta:
        # a_pred < a_act + 129.23 with probability 0.95

        err1 = 2 * N / w
        err2 = self.epsilon * N

        print(f"Markov In.: error less than {err1} with probability: 0.5")
        print(f"CMS Theory: error less than {err2} with probability: {1 - self.delta}")
        print()

        cms_shakespeare = CountMinSketch(w, h) # 272 * 3
        cms_shakespeare.process_stream(corpus)
        cms_shakespeare.get_freq(corpus)

        est_freq = cms_shakespeare.frequencies

        error_freq = self.compute_error(est_freq, actual_freq)
        sorted_freqs = sorted(error_freq.items(), key=lambda x: x[0])

        X, Y = list(zip(*sorted_freqs))

        avg_error = sum(X) / len(X)
        print(f"average error: {avg_error}")
        print()

        acc1 = sum([pair[1] for pair in sorted_freqs if pair[0]<err1])/sum(Y)
        print(f"actual error less than {err1} with probability: {acc1}")

        acc2 = sum([pair[1] for pair in sorted_freqs if pair[0]<err2])/sum(Y)
        print(f"actual error less than {err2} with probability: {acc2}")

        plt.scatter(X, Y)
        plt.show()

# Question 3, 4

def test_1():
    print("Test 1")
    print("epsilon = 0.01, delta = 0.05")
    print(100 * "-")
    test = CMS_Text(0.01, 0.05, 'data\\romeo-and-juliet.txt')
    test.run_and_plot()
    print()

def test_2():
    print("Test 2")
    print("epsilon = 0.005, delta = 0.05")
    print(100 * "-")
    test = CMS_Text(0.005, 0.05, 'data\\romeo-and-juliet.txt')
    test.run_and_plot()
    print()

def test_3():
    print("Test 3")
    print("epsilon = 0.005, delta = 0.001")
    print(100 * "-")
    test = CMS_Text(0.005, 0.01, 'data\\romeo-and-juliet.txt')
    test.run_and_plot()
    print()

def test_4():
    print("Test 4")
    print("epsilon = 0.1, delta = 0.01")
    print(100 * "-")
    test = CMS_Text(0.1, 0.01, 'data\\romeo-and-juliet.txt')
    test.run_and_plot()
    print()

test_1()
test_2()
test_3()
test_4()