from count_min_sketch import CountMinSketch

cms = CountMinSketch(50, 3) # 50 * 3

test1 = []

for i in range(100):
    test1 += i * [f"word{i}"]


cms.process_stream(test1)

cms.get_freq(test1)

print(cms.frequencies)