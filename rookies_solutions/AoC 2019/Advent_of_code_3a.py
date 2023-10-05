import pandas as pd
import numpy as np
import re
import easygui
import os
import math
import copy
import pathlib
from collections import defaultdict

#  set path
path = pathlib.PureWindowsPath(r'C:\Users\boda9003\Desktop\Python_playground\Advent of Code\Inputs\tangled_wires.csv')
print('path used: \n', path)

#  input read out
inputFile = pd.read_csv(path, header=None, sep=";", dtype=str)
#  print('input file used', inputFile)

wireTable = inputFile.transpose()

# print(wireTable)


# get the size of the file
number_of_segments = inputFile.shape[1]
number_of_wires = inputFile.shape[0]

# print(number_of_segments)


# decoding the file into vectors first by direction and distance
# do it in loop
wires = []
for j in wireTable.columns:
    vectors = []
    #print(j)
    for i in wireTable[j]:
        # direction and distance as first letter of the step string
        # vector.loc[number_of_wiresofrow] = InpFil[column][row][number_of_wiresofcharinstring]
        if isinstance(i, str): #not math.isnan(i) or x:
            #print(i,type(i))
            direction = re.match('^[a-zA-Z]', str(i))[0]
            length = int(re.search('[0-9]+', str(i))[0])


        # print(f"{i} translated to  {direction} and {length}\n" )

        vectors.append([direction, length])
    # print(f'vector {j}:',vector)
    wires.append(vectors)

# print('wires: ',wires)


# wires.iat[j,0]=vector#copy.deepcopy(vector)
# wires['totdistance']=

# wires=pd.DataFrame(lista, columns = ('wire','totdist'))

# print for reporting
# print("input in data frame form \n", vector)
# print("wires \n",wires)
# print(wires['wire'][1]['dir'][300])
# print(sum(wires['wire'][0]['dis']))

# print(wires['boundaries'])


# wirepaths = []

# print(wirepaths)
# furthest_point = max(wires['totdist'][0])
# print('Longest wire =', furthest_point)


# wirepaths = pd.DataFrame[columns=[range(number_of_wires)],index=range(furthest_point)]
# for (i=0,i<number_of_segments,i+=1):

# translation to direction vectors
vR = np.array([1, 0])
vL = np.array([-1, 0])
vU = np.array([0, 1])
vD = np.array([0, -1])
v = {'R': vR, 'L': vL, 'U': vU, 'D': vD}  # bylem sprytniejszy niż mi się wydawało

traces = []

for wire_id, wire in enumerate(wires, start=0):
    cursor = np.array([0, 0])
    trace = defaultdict(list)
    travel = 0
    for segment in wire:
        sdir = segment[0]
        sdis = segment[1]

        for k in range(sdis):
            cursor = cursor + v[sdir]
            travel = travel + 1
            trace[str(cursor)].append({'wire': wire_id, "travel": travel})

        # if(i%50==0):
        #   print('wire nr ',j,'laid segment ',cursor)
    traces.append(trace)
# print(traces[0])
print('\n traces DONE')

# print(traces[0])
# print(traces[1])
# result = traces[0].intersection(traces[1])
result = defaultdict(list)

for point in traces[0]:
    if point in traces[1]:
        result[point].append(traces[1][point])
        result[point].append(traces[0][point])

print(result)

shortest_paths = []
for point in result:
    wire0 = result[point][0]
    unpacked0 = min([x['travel'] for x in wire0])
    wire1 = result[point][1]
    unpacked1 = min([x['travel'] for x in wire1])
    shortest_paths.append(unpacked0+unpacked1)



print("shortest path intersection ",min(shortest_paths))
# for point in result:


# str.split

f = lambda x: int(x.strip('[]').split()[0]) + int(x.strip('[]').split()[1])

distances = map(f, result)
closest_point = min(distances)
print("closest point overall", closest_point)

exit(0)
all_segments = []
for j in wires:
    cursor = np.array([0, 0])
    segments = []
    for i in j:
        sdir = i[0]
        sdis = i[1]
        cursor = cursor + v[sdir] * sdis
        segments.append(list(cursor))

        # if(i%50==0):
        #   print('wire nr ',j,'laid segment ',cursor)
    all_segments.append(segments)

print('\n segments DONE')

p1 = np.array([all_segments[0][0][0], all_segments[0][0][1]])
p2 = np.array([all_segments[0][1][0], all_segments[0][1][1]])
p3 = np.array([all_segments[1][0][0], all_segments[1][0][1]])
p4 = np.array([all_segments[1][1][0], all_segments[1][1][1]])

cross1a = np.sign((np.cross(p2 - p1, p3 - p1)))
cross1b = np.sign((np.cross(p2 - p1, p4 - p1)))
cross2a = np.sign((np.cross(p4 - p3, p1 - p3)))
cross2b = np.sign((np.cross(p4 - p3, p2 - p3)))

print(np.sign([cross1a, cross1b, cross2a, cross2b]))

# check for not intersection
if not (cross1a + cross1b in [-2, 2] or cross2a + cross2b in [-2, 2]):
    print('they may intersect')
    if ((cross1a != cross1b & cross1a + cross1b == 0) & (cross2a != cross2b & cross2a + cross2b == 0)):
        print('they for sure intersect')
    elif set([abs(cross1a + cross1b), abs(cross2a + cross2b)]) in [set([1, 0]), set([1, 1])]:
        print('they are edge case')
    elif [cross1a, cross1b, cross2a, cross2b] == [0, 0, 0, 0]:
        print("they are colinear")
        if (max(p1[0], p2[0]) >= max(p3[0], p4[0]) and min(p1[0], p2[0]) <= max(p3[0], p4[0])) or \
                (max(p1[0], p2[0]) <= max(p3[0], p4[0]) and max(p1[0], p2[0]) >= min(p3[0], p4[0])):
            print('and overlapping')
else:
    print('they do not intersect')

print(p1, p2, p3, p4)
# if(sum(np.sign([cross1a,cross1b,cross2a,cross2b])))

print(np.sign(0))

"""
crossings2=[]
i=1
while i < len(all_segments[0]):

    j=1
    p1 =np.array([all_segments[0][i-1][0],all_segments[0][i-1][1]])
    p2 =np.array([all_segments[0][i][0],all_segments[0][i][1]])
    while j<len(all_segments[1]):
        p3 = np.array([all_segments[1][j - 1][0], all_segments[1][j - 1][1]])
        p4 = np.array([all_segments[1][j][0], all_segments[1][j][1]])
        #reduce the vectors
"""

# print('trace',trace)

# for i in

# print('traces: ', traces)
# crossings=[x for x in traces[0] if (x in traces[1]).any()]
"""
crossings=[]
z=0
for i in traces[0]:
    z+=1
    if z%1000 == 0:print(i)
    for j in traces[1]:
        if i==j:
            crossings.append(j)
            break
#crossings = [value for value in traces[0] if value in traces[1]]
#crossings=set(traces[0]).intersect(set(traces[1]))
print(crossings)
"""

"""crossings=[]
for i in traces[0]:
    print(i)
    for j in traces[1]:
        if np.array_equal(i, j):
            crossings.append(j)
            print(j)
            break


print( crossings )
x=np.array([0,990])
#print(x in traces[0])
"""

"""
myarr = np.array([1, 0])
mylistarr = [np.array([1, 2, 3]), np.array([1, 0]), np.array([3.45, 3.2])]

"""

# print(True for elem in mylistarr if elem is myarr0)

# test for identity:
# def is_arr_in_list(myarr, list_arrays):
#   return next((True for elem in list_arrays if elem is myarr), False)

# print('Xs: ',crossings)

# wirepaths = pd.DataFrame(traces,columns=range(number_of_wires))
# print('wirepaths:',wirepaths)

# xmin=furthest_point
# for i in range(furthest_point):
#    try:
#       x=bisect.bisect_left(wirepaths[0],wirepaths[1][i])
#      if x<xmin:
#         xmin=x
# except ValueError:
#   xmin=xmin


# print('xmin',xmin)

"""
minimum_distance=100000
for i in crossings:
    if(minimum_distance>sum(i)):
        minimum_distance=sum(i)
        closest_point=i
print('closest intersection point: ',closest_point)
"""

# input("press enter to exit")
