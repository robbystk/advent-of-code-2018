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

safe_region = set()
safe_region_size = Counter()

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

def is_safe(pt):
    threshold = 10000
    return sum(distances(pt)) < threshold

def add_point_if_safe(pt):
    if is_safe(pt):
        safe_region.add(tuple(pt))

def update_safe_region(pt):
    if is_safe(pt):
        safe_region_size[0] += 1

def add_to_closest_point(pt):
    closest = closest_point(pt)
    if closest is not None:
        areas[closest] += 1

# the set of points we have not reached yet
not_reached = set()
for pt in point_array:
    not_reached.add(tuple(pt))

def remove_point(s, pt):
    """Removes the point pt from the set s"""
    s -= {tuple(pt)}

def is_empty(s):
    """check whether the set is the empty set"""
    return s.issubset({})

def process_point(pt):
    add_to_closest_point(pt)
    add_point_if_safe(pt)
    update_safe_region(pt)

# Traverse out from the center of mass of the array in a diamond-shaped spiral
# counterclockwise.  `direction` is the direction we're moving and is rotated by
# the rotation matrix `rotator` after completing each side.  `increase_radius`
# moves us to the next "ring".  `step_limit` is the number of points in the
# current side, and `step` is how many we've done.

# The strategy will be to go until we've reached all the points in the original
# set (tracked by `not_reached` above) then finish a rotation.  We will save the
# counts at that point, and to one more lap.  Any cells that grow during that
# final lap are assumed to be infinite and removed.  The largest tnon-infinite
# cell corresponds to the point we want.

x_center = int(point_array[:,0].mean())
y_center = int(point_array[:,1].mean())

# constants
direction = np.array([-1,1])
increase_radius = np.array([1,0])
rotator = np.array([[0,1],[-1,0]])
# initial conditions
step_limit = 0
step = 0
side = 0
final_lap = False
done = False
position = np.array([x_center,y_center])
# take care of the first point
process_point(position)
# move to the second point and take care of that as well
position += increase_radius
process_point(position)
while is_safe(position) or not done:
    position += direction
    step += 1
    if step > step_limit:
        direction = direction @ rotator
        step = 0
        side += 1
        if side >= 4:
            # right corner
            position += increase_radius
            step_limit += 1
            side = 0
            if final_lap and not done:
                final_areas = areas.copy()
                done = True
            if is_empty(not_reached):
                final_lap = True
                # save counts
                penultimate_areas = areas.copy()
    # remove the point since we've reached it
    remove_point(not_reached, position)
    # update areas
    process_point(position)

finite_areas = final_areas.copy()

for i in final_areas:
    if final_areas[i] > penultimate_areas[i]:
        del finite_areas[i]

print(finite_areas.most_common(1))

# print(safe_region)
print(safe_region_size)

# plot safe region
x,y = list(zip(*safe_region))
plt.plot(x,y, '.')
plt.show()
