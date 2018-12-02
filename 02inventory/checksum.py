import sys

with open(sys.argv[1]) as f:
    box_id_list = [line.strip() for line in f]

def letter_counts(box_id):
    counts = {chr(c): 0 for c in range(ord('a'), ord('z') + 1)}
    for c in box_id:
        counts[c] += 1
    return counts

def contains_exactly(n, counts):
    for letter, count in counts.items():
        if count == n:
            return True
    return False

def checksum(id_list):
    twos = 0
    threes = 0
    for box_id in id_list:
        counts = letter_counts(box_id)
        if contains_exactly(2, counts):
            twos += 1
        if contains_exactly(3, counts):
            threes += 1
    checksum = twos * threes
    return checksum

print(checksum(box_id_list))
