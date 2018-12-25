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

path = np.array([[x_center],[y_center]])
direction = np.array([[1,0]])
rotator = np.array([[0,1],[-1,0]])
step_limit = 1
step = 0
for i in range(300):
    path = np.append(path, (path[:,-1] + direction).T, axis=1)
    step += 1
    if step == step_limit:
        step = 0
        if direction[0,0] == 0:
            step_limit += 1
        direction = direction @ rotator

plt.plot(path[0,:], path[1,:])
plt.show()
plt.close()
