import sys
import re
import numpy as np
import matplotlib.pyplot as plt

coordinate_pattern = re.compile("^([0-9]+), ([0-9]+)$")

with open(sys.argv[1]) as f:
    points = []
    for line in f:
        match = coordinate_pattern.match(line)
        if match:
            points.append([int(match.group(1)), int(match.group(2))])
        else:
            print("could not parse line", file=sys.stderr)

points = np.array(points)

plt.scatter(points[:,0], points[:,1])
# plt.show()
# plt.close()

x_center = int(points[:,0].mean())
y_center = int(points[:,1].mean())

direction = np.array([-1,1])
increase_radius = np.array([1,0])
rotator = np.array([[0,1],[-1,0]])
step_limit = 0
step = 0
side = 0
position = np.array([x_center,y_center])
path = [position.flatten().tolist()]
position += increase_radius
path.append(position.flatten().tolist())
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
    path.append(position.flatten().tolist())

path = np.array(path)
# print(path - [x_center, y_center])

plt.plot(path[:,0], path[:,1], '.-')
plt.show()
plt.close()
