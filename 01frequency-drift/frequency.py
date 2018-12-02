import sys

with open(sys.argv[1]) as f:
    deltas = [int(line) for line in f.readlines()]

frequency = 0               # starting frequency
frequency_set = set([0])    # a set to keep track of what frequencies we've seen
repeated = False            # whether we've seen a frequency twice
repeated_frequency = None   # the first frequency we've seen twice
final_frequency = None      # the frequency after the first pass through the input
first_repetition = True     # whether we're on that first pass
while not repeated:
    for delta in deltas:
        frequency += delta
        # check if we've seen this frequency before
        if frequency in frequency_set and not repeated:
            repeated_frequency = frequency
            repeated = True
        # record the frequency in case we see it again
        frequency_set.add(frequency)

    # when we've finished the first pass, we need to record the frequency
    # reached and make sure we don't alter it further
    if first_repetition:
        final_frequency = frequency
        first_repetition = False

print("final frequency: %d" % final_frequency)
if repeated:
    print("first repeated frequency: %d" % repeated_frequency)
