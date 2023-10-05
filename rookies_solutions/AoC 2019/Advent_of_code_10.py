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


def cast_a_ray(mdist_max, point):
    mlt = 1
    stops = []
    while sum(point * mlt) <= mdist_max:
        stops.append(tuple([x * mlt for x in point]))
        mlt += 1

    return stops


def adress_metric(mdist, mdist_max, primes_list, coverage_list):
    adres_quad = []
    for x in range(mdist + 1):
        xc = x #mdist + 1 - x
        yc = mdist + 1 - x
        if (xc, yc) not in coverage_list:  # ( 0 in [xc % k + yc % k for k in range(2, min((yc+1,xc+1)))]
            # print("casting a ray from ",xc, yc)
            ray = cast_a_ray(mdist_max, (xc, yc))
            # print(ray)
            adres_quad.append(ray)
    # prune the duplicated rays

    adres_circ = adres_quad.copy()
    for o in range(3):
        adres_quad = [[(z[1], -z[0]) for z in y] for y in adres_quad]
        adres_circ.extend(adres_quad)

    return adres_circ


def primes(n):
    """ Returns  a list of primes < n """
    sieve = [True] * n
    for i in range(3, int(n ** 0.5) + 1, 2):
        if sieve[i]:
            sieve[i * i::2 * i] = [False] * ((n - i * i - 1) // (2 * i) + 1)
    return [2] + [i for i in range(3, n, 2) if sieve[i]]


# list_of_tuples = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (0, 11), (0, 12),
#                  (0, 13), (0, 14), (0, 15), (0, 16), (0, 17), (0, 18), (0, 19), (0, 20), (0, 2)]


# string1 = "ABAKUS"
# L = 10
# string1 = string1[:L] + "." + string1[L + 1:]
# print( (0,1) in list_of_tuples)
# print(string1)
# exit(0)

# get list of primes for faster ray origin checking
maxd = 40
primes_list = [1]
primes_list.extend(list(primes(maxd)))

# initiate and execute the raycasting
rombo = []
flatrombo = []
for z in range(maxd):

    portion = adress_metric(z, maxd, primes_list, flatrombo)
    rombo.extend(portion)
    for x in portion:
        flatrombo.extend(x)
    # print(flatrombo)

# print(primes_list)
# print(rombo)
# print("last element")
# print(rombo[-1])
print("rays precasted:", len(rombo))
print("points covered:", sum([len(x) for x in rombo]))

# print (flatrombo)
print("duplicated points in rombo", [item for item, count in collections.Counter(flatrombo).items() if count > 1])

# exit(0)
mapstring = """.###..#######..####..##...#
########.#.###...###.#....#
###..#...#######...#..####.
.##.#.....#....##.#.#.....#
###.#######.###..##......#.
#..###..###.##.#.#####....#
#.##..###....#####...##.##.
####.##..#...#####.#..###.#
#..#....####.####.###.#.###
#..#..#....###...#####..#..
##...####.######....#.####.
####.##...###.####..##....#
#.#..#.###.#.##.####..#...#
..##..##....#.#..##..#.#..#
##.##.#..######.#..#..####.
#.....#####.##........#####
###.#.#######..#.#.##..#..#
###...#..#.#..##.##..#####.
.##.#..#...#####.###.##.##.
...#.#.######.#####.#.####.
#..##..###...###.#.#..#.#.#
.#..#.#......#.###...###..#
#.##.#.#..#.#......#..#..##
.##.##.##.#...##.##.##.#..#
#.###.#.#...##..#####.###.#
#.####.#..#.#.##.######.#..
.#.#####.##...#...#.##...#."""

maplist = str.split(mapstring, "\n")
# print("".join(map))
mapsize = len(maplist)
print("mapsize", mapsize, len(maplist[0]))

print(len([x for x in mapstring if x == "#"]))

# print(map[9][-10])

# exit(0)
# stationy=0
# stationx=6

raport = []  # {"x":0,"y",0,"count":0}
xrep = 0
yrep = 0
countrep = 0
for y, yrow in enumerate(maplist):
    for x, xcol in enumerate(yrow):
        if yrow[x] == "#":
            # print("analysing:", x, y)
            counter = 0
            for ray in rombo:
                for point in ray:
                    try:
                        # print("checking ", point[1]+y,point[0]+x)

                        targety = point[1] + y
                        targetx = point[0] + x
                        if targetx >= 0 and targety >= 0 and maplist[targety][targetx] == "#":
                            counter += 1
                            break
                    except IndexError:
                        break
            # raport.append("#")
            # raport = raport + "#"
            raport.append({"x": x, "y": y, "count": counter})
            # print("asteroid", x, y, counter)
            if counter > countrep:
                xrep = x
                yrep = y
                countrep = counter

        elif yrow[x] == ".":
            pass
            # print("station can not be placed at space",stationx,stationy)
            # raport = raport+"."

# print(raport)

print("asteroid", xrep, yrep, countrep)

rombos = [  [(x,y) for x,y in ray ] for ray in rombo]

print (rombos)
def keyfunction(xlo):
    x =-xlo[0][1]
    y= xlo[0][0]

    z = math.atan2(y, x) / math.pi
    if z<0:
        z=z+2

    # print((x, y), z)

    return z  # -  math.pi/2


print(rombo)

rombos = sorted(rombos, key=keyfunction ) #, reverse=True)
print(rombos)

#xrep = 8
#yrep = 3

print("shooting from:", xrep, yrep)
counter = 0
destroyed = []
notemptyrun = 1
while notemptyrun:
    notemptyrun = 0
    for i, ray in enumerate(rombos):
        for point in ray:
            try:
                # print("checking ", point[1]+y,point[0]+x)

                targety = point[1] + yrep
                targetx = point[0] + xrep
                if targetx >= 0 and targetx <= mapsize and targety >= 0 and targety <= mapsize and maplist[targety][targetx] == "#":
                    counter += 1
                    # map[targety][targetx] = "."
                    maplist[targety] = maplist[targety][:targetx] + "." + maplist[targety][targetx + 1:]
                    destroyed.append((targetx, targety))
                    print((targetx, targety),counter)
                    notemptyrun = 1
                    break
            except IndexError:

                break
    # raport.append("#")
    # raport = raport + "#"
    raport.append({"x": x, "y": y, "count": counter})



#exit(0)
testrange = range(100)

testfi = [x/100*2*math.pi for x in testrange]
testx = [math.cos(x) for x in testfi]
testy = [math.sin(x) for x in testfi]

testcords = zip(testy,testx)
print(testcords)



testatan = [math.atan2(y,x) for y,x in testcords]
testatan2 = [x+2*math.pi if x < 0 else x for x in testatan ]

# testy = math.atan2()
#
# print(1,0,math.atan2(1,0))
# print(1,1,math.atan2(1,1))
# print(0,1,math.atan2(0,1))
# print(-1,1,math.atan2(-1,1))
#
# print(-1,0,math.atan2(-1,0))
# print(-1,-1,math.atan2(-1,-1))
#
# print(0,-1,math.atan2(0,-1))
# print(1,-1,math.atan2(1,-1))

# print(0,-1,math.atan2(0,-1)/math.pi)
# print(1,0,math.atan2(1,0)/math.pi)
# print(-1,0,math.atan2(-1,0)/math.pi)

#exit(0)

# exit(0)
#x = np.array([x[0] for x in destroyed])
#y = np.array([x[1] for x in destroyed])

#x = np.array(testrange)

#y = np.array(testatan2)

#fig, ax = plt.subplots()
#ax.set(xlabel='x', ylabel='y',
#       title='About as simple as it gets, folks')
#ax.grid()

#plt.show()

# for i,ray in enumerate(rombos):
# # Data for plotting
#     x = np.array([z[0] for z in ray])  # [z[0] for z  in [j for j in rombo]])
#     y = np.array([z[1] for z in ray])  # [z[1] for z  in [j for j in rombo]])  # 1 + np.sin(2 * np.pi * t)
#     ax.plot(x, y, marker='o')
#     time.sleep(0.2)
#     if i/len(rombos) > 1/6:
#         break

#ax.plot(x, y, marker='o')


# ax.set_ylim(ymin=-1)
# ax.set_xlim(xmin=-1)

# fig.savefig("test.png")

#exit(0)

import matplotlib.pyplot as plt



pi = 3.14159

fig, ax = plt.subplots()

x = []
y = []

def PointsInCircum(r,n=20):
    circle = [(math.cos(2*pi/n*x)*r,math.sin(2*pi/n*x)*r) for x in range(0,n+1)]
    return circle

circle_list = PointsInCircum(3, 50)

ax.set_xlim(-mapsize, mapsize)
ax.set_ylim(-mapsize, mapsize)

for i,ray in enumerate(rombos):
    #x_coord, y_coord = circle_list.pop()
    #x.extend(x_coord)
    #y.extend(y_coord)

    x = np.array([z[0] for z in ray])
    y = np.array([z[1] for z in ray])
    print(list(zip(x,y)))
    ax.plot(x, y,marker='o')
    plt.pause(0.01)

#
# # Data for plotting
#     x = np.array([z[0] for z in ray])  # [z[0] for z  in [j for j in rombo]])
#     y = np.array([z[1] for z in ray])  # [z[1] for z  in [j for j in rombo]])  # 1 + np.sin(2 * np.pi * t)
#     ax.plot(x, y, marker='o')
#     time.sleep(0.2)
#     if i/len(rombos) > 1/6:
#         break