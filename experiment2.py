from math import ceil
import math
import re
from matplotlib import pyplot as plt
from count_min_sketch import CountMinSketch

# Experiment 2 (Shakespeare)

with open('data\\romeo-and-juliet.txt', 'r') as file:
    raw = file.read().replace('\n', ' ')
    corpus = re.sub(r'[^A-Za-z0-9 ]+', '', raw).lower().split()

actual_freq = {}

for word in corpus:
    if word not in actual_freq:
        actual_freq[word] = 1
    else:
        actual_freq[word] += 1

N = sum(actual_freq.values())

print(f"Number of unique words: {len(actual_freq)}")
print(f"Number of words, total: {N}")
print()

# sigma = 0.005
sigma = 0.01
w = ceil(math.e / sigma) # 272
print(f"width: {w}")

delta = 0.05
h = ceil(math.log(1/delta)) # 3
print(f"height: {h}")

print()

# estimate less than sigma * N with probability 1 - delta:
# a_pred < a_act + 129.23 with probability 0.95

err1 = 2 * N / w
err2 = sigma * N

print(f"Markov In.: error less than {err1} with probability: 0.5")
print(f"CMS Theory: error less than {err2} with probability: {1 - delta}")
print()

cms_shakespeare = CountMinSketch(w, h) # 272 * 3
cms_shakespeare.process_stream(corpus)
cms_shakespeare.get_freq(corpus)

est_freq = cms_shakespeare.frequencies

error_freq = {}

for word in actual_freq:
    diff = est_freq[word] - actual_freq[word]
    if diff not in error_freq:
        error_freq[diff] = 1
    else:
        error_freq[diff] += 1

sorted_freqs = sorted(error_freq.items(), key=lambda x: x[0])

X, Y = list(zip(*sorted_freqs))

avg_error = sum(Y) / len(Y)
print(f"average error: {avg_error}")
print()

acc1 = sum([pair[1] for pair in sorted_freqs if pair[0]<err1])/sum(Y)
print(f"actual error less than {err1} with probability: {acc1}")

acc2 = sum([pair[1] for pair in sorted_freqs if pair[0]<err2])/sum(Y)
print(f"actual error less than {err2} with probability: {acc2}")

plt.scatter(X, Y)
plt.show()