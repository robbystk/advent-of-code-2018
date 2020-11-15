import sys

def input():
    with open(sys.argv[1]) as f:
        for token in f.read().split(' '):
            yield token

class Node:
    def __init__(self, input):
        self.children_count = int(next(input))
        self.metadata_count = int(next(input))

        self.children = [Node(input) for _ in range(self.children_count)]
        self.metadata = [int(next(input)) for _ in range(self.metadata_count)]

    def __repr__(self):
        children_str = ''.join([repr(child) for child in self.children])
        return f"<node metadata=\"{self.metadata}\">{children_str}</node>"

    def metadata_sum(self):
        return sum([child.metadata_sum() for child in self.children]) + sum(self.metadata)

    def value(self):
        if self.children_count == 0:
            value = sum(self.metadata)
            return value
        else:
            rv = 0
            for idx in self.metadata:
                if idx > 0 and idx <= self.children_count:
                    rv += self.children[idx - 1].value()
            return rv

def main():
    inp = input()
    root = Node(inp)

    try:
        print(next(inp))
    except StopIteration as e:
        pass
    else:
        raise "didn't reach end of input"

    print(f"metadata sum: {root.metadata_sum()}")

    print(f"value: {root.value()}")

if __name__ == '__main__':
    main()
