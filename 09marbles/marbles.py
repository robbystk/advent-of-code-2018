import sys

def params():
    return (int(sys.argv[1]), int(sys.argv[2]))

class Circle:
    def __init__(self):
        self.circle = [0]
        self.current_marble_idx = 0

    def play(self, marble_num, player):
        if marble_num % 23 == 0:
            player.add_points(marble_num)
            self.current_marble_idx = (self.current_marble_idx - 7) % len(self.circle)
            player.add_points(self.circle.pop(self.current_marble_idx))
        else:
            self.current_marble_idx = (self.current_marble_idx + 2) % len(self.circle)
            self.circle.insert(self.current_marble_idx, marble_num)

    def __repr__(self):
        rv = []
        for i, marble in enumerate(self.circle):
            if i == self.current_marble_idx:
                rv.append(f"({marble})")
            else:
                rv.append(str(marble))
        return ', '.join(rv)

class Players:
    def __init__(self, player_count):
        self.player_count = player_count
        self.players = [Player() for _ in range(player_count)]
        self.current_idx = 0

    def __next__(self):
        self.current_idx = (self.current_idx + 1) % self.player_count
        return self.players[self.current_idx]

    def winner(self):
        winner = None
        high_score = 0
        for player in self.players:
            if player.score > high_score:
                high_score = player.score
                winner = player

        return winner

    def __repr__(self):
        return ', '.join([f"{idx}: {self.players[idx].score}" for idx in range(self.player_count)])

class Player:
    def __init__(self):
        self.score = 0

    def add_points(self, points):
        self.score += points

def main():
    player_count, last_marble = params()

    circle = Circle()
    players = Players(player_count)

    for marble in range(1, last_marble + 1):
        player = next(players)
        circle.play(marble, player)

    winner = players.winner()
    print(winner.score)

if __name__ == '__main__':
    main()
