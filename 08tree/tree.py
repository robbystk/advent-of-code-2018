import sys

def input():
    with open(sys.argv[1]) as f:
        for token in f.read().split(' '):
            yield token

class Node:
    def __init__(self, input):
        children_count = int(next(input))
        metadata_count = int(next(input))

        self.children = [Node(input) for _ in range(children_count)]
        self.metadata = [int(next(input)) for _ in range(metadata_count)]

    def __repr__(self):
        return f"Children:\n\t{self.children}\nMetadata:\n\t{self.metadata}\n"

    def metadata_sum(self):
        return sum([child.metadata_sum() for child in self.children]) + sum(self.metadata)

def main():
    inp = input()
    root = Node(inp)

    print(root.metadata_sum())

if __name__ == '__main__':
    main()
