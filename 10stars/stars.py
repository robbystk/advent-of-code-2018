import sys

import re
import numpy as np

def input():
    with open(sys.argv[1]) as f:
        for line in f:
            yield line

class Stars:
    def __init__(self, position_list, velocity_list):
        self.position_list = np.array(position_list)
        self.velocity_list = np.array(velocity_list)

    def advance(self):
        self.position_list += self.velocity_list

    def bounding_box_size(self):
        return self.position_list.max(axis=0) - self.position_list.min(axis=0)

    def __str__(self):
        start = self.position_list.min(axis=0) - np.array([1, 1])
        end = self.position_list.max(axis=0) + np.array([1, 1])
        dimensions = self.bounding_box_size() + np.array([2,2])

        picture = [[' ' for _ in range(dimensions[0])] for _ in range(dimensions[1])]

        for position in self.position_list:
            offset_position = position - start
            picture[offset_position[1]][offset_position[0]] = '#'

        return '\n'.join([''.join(row) for row in picture])


def main():
    line_pattern = re.compile('\Aposition=< *(-?\d+),  *(-?\d+)> velocity=< *(-?\d+),  *(-?\d+)>')

    position_list = []
    velocity_list = []

    for line in input():
        matches = line_pattern.match(line)
        (x_pos, y_pos, x_vel, y_vel) = matches.group(1, 2, 3, 4)
        position_list.append([int(x_pos), int(y_pos)])
        velocity_list.append([int(x_vel), int(y_vel)])

    starfield = Stars(position_list, velocity_list)
    
    print(starfield.bounding_box_size())

    print(starfield)

if __name__ == '__main__':
    main()
