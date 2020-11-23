import sys

import numpy as np

def grid_serial_number():
    return int(sys.argv[1])

class Grid:
    def __init__(self, serial_number):
        self.serial_number = serial_number
        self.power_map = Grid.populate_power_map(serial_number)

    def square_power_level(self, top_left_x, top_left_y, square_size=3):
        rv = 0
        for x in range(top_left_x, top_left_x + square_size):
            for y in range(top_left_y, top_left_y + square_size):
                rv += self.power_level(x, y)
        return rv

    def power_level(self, x, y):
        # fuel cells are indexed from 1, but the power map is indexed from zero
        return self.power_map[x - 1, y - 1]

    def cell_power(x, y, serial_number):
        rack_id = x + 10
        power_level = rack_id * y + serial_number
        power_level *= rack_id
        power_level = (power_level // 100) % 10 # keep hundreds digit
        power_level -= 5
        return power_level

    def populate_power_map(serial_number):
        power_map = np.empty((300, 300), dtype=np.int8)
        for x in range(300):
            for y in range(300):
                # fuel cells are indexed from 1,
                # but the power map is indexed from zero
                power_map[x,y] = Grid.cell_power(x + 1, y + 1, serial_number)

        return power_map

    def show_region(self, top_left_x, top_left_y, square_size=3):
        region = []
        for y in range(top_left_y - 1, top_left_y + square_size + 1):
            region.append([])
            for x in range(top_left_x - 1, top_left_x + square_size + 1):
                power_level = self.power_level(x, y)
                region[-1].append(f"{power_level: 3}")

        return '\n'.join(['  '.join(row) for row in region])

    def find_max_power_square(self):
        max_power = -5 * 300**2
        max_params = (None, None, None)

        for square_size in range(1, 300 + 1):
            for x in range(1, 300 - square_size + 1):
                for y in range(1, 300 - square_size + 1):
                    power = self.square_power_level(x, y, square_size)
                    if power > max_power:
                        max_power = power
                        max_coords = (x, y, square_size)
        return max_coords

def main():
    grid = Grid(grid_serial_number())

    max_x, max_y, square_size = grid.find_max_power_square()

    print(f"max square is: ({max_x},{max_y},{square_size})")

    print(grid.show_region(max_x, max_y, square_size))

if __name__ == '__main__':
    main()
