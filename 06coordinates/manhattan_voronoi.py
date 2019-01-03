import sys
import re
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

coordinate_pattern = re.compile("^([0-9]+), ([0-9]+)$")

with open(sys.argv[1]) as f:
    point_array = []
    for line in f:
        match = coordinate_pattern.match(line)
        if match:
            point_array.append([int(match.group(1)), int(match.group(2))])
        else:
            print("could not parse line", file=sys.stderr)

point_array = np.array(point_array)

# how many points are closest to each point
areas = Counter()

plt.scatter(point_array[:,0], point_array[:,1])
# plt.show()

plt.close()

def manhattan_distance(pt1, pt2):
    return abs(pt1[0] - pt2[0]) + abs(pt1[1] - pt2[1])

def distances(pt):
    return ([manhattan_distance(p, pt) for p in point_array])

def closest_point(pt):
    closest = second = float("inf")
    closest_index = None
    for i,d in enumerate(distances(pt)):
        if d <= closest:
            closest, second = d, closest
            closest_index = i
    if closest == second:
        return None
    else:
        return closest_index


def add_to_closest_point(pt):
    closest = closest_point(pt)
    if closest is not None:
        areas[closest] += 1

x_center = int(point_array[:,0].mean())
y_center = int(point_array[:,1].mean())

direction = np.array([-1,1])
increase_radius = np.array([1,0])
rotator = np.array([[0,1],[-1,0]])
step_limit = 0
step = 0
side = 0
position = np.array([x_center,y_center])
add_to_closest_point(position)
position += increase_radius
add_to_closest_point(position)
for i in range(1,300):
    position += direction
    step += 1
    if step > step_limit:
        direction = direction @ rotator
        step = 0
        side += 1
        if side >= 4:
            position += increase_radius
            step_limit += 1
            side = 0
    add_to_closest_point(position)

print(areas.most_common(1)[0])
