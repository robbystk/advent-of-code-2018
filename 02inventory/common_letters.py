import sys

with open(sys.argv[1]) as f:
    box_id_list = [line.strip() for line in f]

def similar_pair(id_list):
    for i in range(len(id_list)):
        for j in range(i, len(id_list)):
            if uncommon_letter_count(id_list[i], id_list[j]) == 1:
                return (id_list[i], id_list[j])

def uncommon_letter_count(str1, str2):
    count = 0
    for c1,c2 in zip(str1, str2):
        if c1 != c2:
            count += 1
    return count

def print_common_letters(strings):
    for c1, c2 in zip(strings[0], strings[1]):
        if c1 == c2:
            print(c1, end='')
    print('')

print_common_letters(similar_pair(box_id_list))
