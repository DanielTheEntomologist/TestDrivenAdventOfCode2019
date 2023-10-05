import pandas as pd
# import easygui
# import os
import math
import time
import copy
from pathlib import PureWindowsPath
# from collections import deque
import collections
# import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict


class bodyClass:
    """body in the pseudo3body problem"""

    def __init__(self, coords, vel, name):
        self.name = name
        self.coords = coords
        self.vel = vel
        self.inicoords = coords.copy()
        self.inivel = vel.copy()
        # self.y = y
        # self.z = z
        # self.vx = vx
        # self.vy = vy
        # self.vz = vz

    def pull(self, list_of_bodies):

        for body in list_of_bodies:
            for i, coord in enumerate(self.coords):
                if coord < body.coords[i]:
                    body.vel[i] += -1
                elif coord > body.coords[i]:
                    body.vel[i] += 1
                else:
                    pass

    def move(self):
        for i, coord in enumerate(self.coords):
            self.coords[i] += self.vel[i]

    def kinetic(self):
        return sum([abs(p) for p in self.vel])

    def potential(self):
        return sum([abs(p) for p in self.coords])

    def total(self):
        return self.kinetic() * self.potential()

    def checknostalgia(self):
        velnost = (x == y for x, y in zip(self.inivel, self.vel))
        coordnost = (x == y for x, y in zip(self.inicoords, self.coords))

        if any(velnost) and any(coordnost):
            # print(velnost, coordnost)
            velcheck = [x == y for x, y in zip(self.inivel, self.vel)]
            cordcheck = [x == y for x, y in zip(self.inicoords, self.coords)]
            indexes = [x and y for x, y in zip(velcheck, cordcheck)]
            # print(indexes)
            return np.array(indexes)
        return None


# actual puzzle
Io = bodyClass([13, -13, -2], [0, 0, 0], "Io")
Europa = bodyClass([16, 2, -15], [0, 0, 0], "Europa")
Ganymede = bodyClass([7, -18, -12], [0, 0, 0], "Ganymede")
Callisto = bodyClass([-3, -8, -8], [0, 0, 0], "Callisto")

# test 1 input
# Io = bodyClass([-1, 0, 2], [0, 0, 0],"Io")
# Europa = bodyClass([2, -10, -7], [0, 0, 0],"Europa")
# Ganymede = bodyClass([4, -8, 8], [0, 0, 0],"Ganymede")
# Callisto = bodyClass([3, 5, -1], [0, 0, 0],"Callisto")

# test 2 input - really long return
# Io = bodyClass([-8,-10, 0], [0, 0, 0])
# Europa = bodyClass([5, 5, 10], [0, 0, 0])
# Ganymede = bodyClass([2, -7, 3], [0, 0, 0])
# Callisto = bodyClass([9, -8, -3], [0, 0, 0])

list_of_moons = [Io, Europa, Ganymede, Callisto]

time_0 = time.time()

# finish_line = 295693702908636

# Io_trace = []
# Europa_trace = []
# Ganymede_trace = []
# Callisto_trace = []
# steps = []
periods = []
trace = defaultdict(list)

k = 1
while True:

    # print("===============================\n step", k)

    # energy = 0
    # center_of_gravity = [0, 0, 0]
    # total_velocity = [0, 0, 0]

    for moon in list_of_moons:
        #   trace[moon.name].append([moon.kinetic(), moon.potential(), moon.total()])
        moon.pull(list_of_bodies=list_of_moons)

    for moon in list_of_moons:
        moon.move()

        # energy = energy + moon.total()
        #    print(moon.coords, moon.vel, moon.total())
        # center_of_gravity = [center_of_gravity[i] + cord for i, cord in enumerate(moon.coords)]
        # total_velocity = [total_velocity[i] + vel for i, vel in enumerate(moon.vel)]

    # trace["total_energy"].append(energy)
    # print("energy total:", energy)
    # print("center of gravity:",center_of_gravity)
    # print("total_velocity:", total_velocity)

    # if any(moon.checknostalgia() for moon in list_of_moons):
    #     for bod in list_of_moons:
    #         if bod.checknostalgia():
    #             periods.append([bod.name, k])
    #             print(periods)

    if any(moon.checknostalgia() is None for moon in list_of_moons):
        pass
    else:
        checks = []
        for moon in list_of_moons:
            checks.append(moon.checknostalgia())
            verdict = [True, True, True]
            for i, check in enumerate(checks):
                verdict = np.logical_and(verdict, check)

        if any(verdict):
            print(verdict, k)
            periods.append([list(verdict), k])
            stopper = [False, False, False]
            for period in periods:
                stopper = np.logical_or(stopper, period[0])
            if all(stopper):
                break

    # print(numpay)

    # print(np.logical_and([numpay]))

    # if all(moon.checknostalgia() for moon in list_of_moons):
    #    print("The end is the beginning and the beginning is the end!")
    #    print(k)
    #    break

    k += 1
    # if k % 100000 == 0:
    #     time_elapsed = time.time() - time_0
    #     ETA = time_elapsed / (k / finish_line) - time_elapsed
    #     print(ETA / 3600)

print(periods)
alreadythere = [[], []]
for period in periods:
    i = period[0].index(True)
    # print(i)
    if i not in alreadythere[0]:
        alreadythere[0].append(i)
        alreadythere[1].append(period[1])

print(alreadythere)

# print(math.lcm(alreadythere[1]))
# print(trace["Io"])

# [x,y in ]

import functools


def lcm(numbers):
    return functools.reduce(lambda x, y: (x * y) / math.gcd(x, y), numbers, 1)


x1 = alreadythere[1][0]
x2 = alreadythere[1][1]
x3 = alreadythere[1][2]

print(x1, x2, x3)

from math import gcd

a = [x1, x2, x3]  # will work for an int array of any length
lcm = a[0]
for i in a[1:]:
    lcm = lcm * i // gcd(lcm, i)
print(lcm)

# print( compute_lcm(200,400) )

exit(0)
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

x = []
y = []
# ax.set_xlim(-mapsize, mapsize)
# ax.set_ylim(-mapsize, mapsize)

# for x in trace["Io"]:
# x_coord, y_coord = circle_list.pop()
# x.extend(x_coord)
# y.extend(y_coord)


# x = np.array([x[0] for z in ray])
k = np.array([x[0] for x in trace["Io"]])
p = np.array([x[1] for x in trace["Io"]])
t = np.array([x for x in trace["total_energy"]])
# ax.plot( k, marker='o')
# ax.plot( p, marker='x')
ax.plot(t, marker='o')
plt.pause(100)
# plt.display()
#
# # Data for plotting
#     x = np.array([z[0] for z in ray])  # [z[0] for z  in [j for j in rombo]])
#     y = np.array([z[1] for z in ray])  # [z[1] for z  in [j for j in rombo]])  # 1 + np.sin(2 * np.pi * t)
#     ax.plot(x, y, marker='o')
#     time.sleep(0.2)
#     if i/len(rombos) > 1/6:
#         break
