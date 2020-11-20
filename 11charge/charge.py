import sys

def grid_serial_number():
    return int(sys.argv[1])

class Grid:
    def __init__(self, serial_number):
        self.power_map = {}
        self.serial_number = serial_number

    def square_power_level(self, top_left_x, top_left_y):
        rv = 0
        for x in range(top_left_x, top_left_x + 3):
            for y in range(top_left_y, top_left_y + 3):
                rv += self.power_level(x, y)
        return rv

    def power_level(self, x, y):
        if (x, y) in self.power_map:
            return self.power_map[(x, y)]
        else:
            level = Grid.cell_power(x, y, self.serial_number)
            self.power_map[(x, y)] = level
            return level

    def cell_power(x, y, serial_number):
        rack_id = x + 10
        power_level = rack_id * y + serial_number
        power_level *= rack_id
        power_level = (power_level // 100) % 10 # keep hundreds digit
        power_level -= 5
        return power_level

    def show_region(self, top_left_x, top_left_y):
        region = []
        for y in range(top_left_y - 1, top_left_y + 4):
            region.append([])
            for x in range(top_left_x - 1, top_left_x + 4):
                power_level = self.power_level(x, y)
                region[-1].append(f"{power_level: 3}")

        return '\n'.join(['  '.join(row) for row in region])

    def find_max_power_square(self):
        max_power = -45
        max_coords = (None, None)

        for x in range(1, 300 - 3 + 1):
            for y in range(1, 300 - 3 + 1):
                power = self.square_power_level(x, y)
                if power > max_power:
                    max_power = power
                    max_coords = (x, y)
        return max_coords

def main():
    grid = Grid(grid_serial_number())

    max_x, max_y = grid.find_max_power_square()

    print(f"max square at: ({max_x}, {max_y})")

    print(grid.show_region(max_x, max_y))

    print(grid.square_power_level(max_x, max_y))


if __name__ == '__main__':
    main()
