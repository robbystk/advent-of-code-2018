import sys

class Params:
    def __init__(self, players, marble_count):
        self.players = players
        self.marble_count = marble_count

    def __repr__(self):
        return str(self.__dict__)

def params():
    return Params(int(sys.argv[1]), int(sys.argv[2]))

def main():
    print(params())

if __name__ == '__main__':
    main()
