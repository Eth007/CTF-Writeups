#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

lines = [l.strip() for l in open("coordinates.txt").readlines()][::-1]

coords = []

for n in range(len(lines)//3):
  coords.append([int(lines.pop().replace("X: ", "")), int(lines.pop().replace("Y: ", "")), int(lines.pop().replace("Z: ", ""))])

fig = plt.figure()
ax = plt.axes()

for n in coords:
  if n[0] < -350 and n[0] > -380:
    plt.plot(-n[2], n[1], 'ro', markersize=2)

ax.set_aspect("equal", "box")

plt.show()
