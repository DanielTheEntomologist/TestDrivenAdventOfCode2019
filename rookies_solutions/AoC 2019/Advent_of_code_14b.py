import pandas as pd
# import easygui
# import os
import math
import copy
from pathlib import PureWindowsPath
from collections import deque
from collections import defaultdict
from collections import Counter
# import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def produce(substance, units_required, cookbook_in, leftovers):
    if substance == 'ORE':
        #if units_required <= leftovers[substance]:
       return units_required
        #else:
         #   return None

    # get recipe
    recipe = [recipe for recipe in cookbook_in if recipe[0][1] == substance]
    units_rec = int(recipe[0][0][0])

    # consume leftovers
    if leftovers[substance] >= units_required:
        leftovers[substance] = leftovers[substance] - units_required
        return 0
    elif leftovers[substance] < units_required:
        units_required = units_required - leftovers[substance]
        leftovers[substance] = 0

    multi = math.ceil(units_required / units_rec)
    units_to_produce = multi * units_rec

    leftovers[substance] += units_to_produce - units_required

    substrates = [x for x in recipe[0][1]]
    orereq = 0

    # print("producing", substance, units_required, units_to_produce)
    for coef, substrate in substrates:
        # print("Require:", substrate, multi * int(coef))

        orereq += produce(substrate, multi * int(coef), cookbook_in, leftovers)
        #if produ is not None:
       #     orereq += produ
    return orereq


# 165
# rawcookbook = """9 ORE => 2 A
# 8 ORE => 3 B
# 7 ORE => 5 C
# 3 A, 4 B => 1 AB
# 5 B, 7 C => 1 BC
# 4 C, 1 A => 1 CA
# 2 AB, 3 BC, 4 CA => 1 FUEL"""

# 31
# rawcookbook = """10 ORE => 10 A
# 1 ORE => 1 B
# 7 A, 1 B => 1 C
# 7 A, 1 C => 1 D
# 7 A, 1 D => 1 E
# 7 A, 1 E => 1 FUEL"""

# 13312
# rawcookbook = """157 ORE => 5 NZVS
# 165 ORE => 6 DCFZ
# 44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
# 12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
# 179 ORE => 7 PSHF
# 177 ORE => 5 HKGWZ
# 7 DCFZ, 7 PSHF => 2 XJWVT
# 165 ORE => 2 GPVTF
# 3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"""

# pucle input

rawcookbook = """6 WBVJ, 16 CDVNK => 2 PJBZT
135 ORE => 8 MWDXJ
27 NBRHT, 2 NSWK, 2 CMHMQ, 29 NFCB, 11 KNGJ, 12 MGCKC, 56 NHTKL, 7 WNFSV => 1 FUEL
1 SFJFX, 3 MXNK => 4 NLSBZ
2 PFKRW, 1 VXFRX, 22 QDJCL => 6 GBDG
7 TSTF, 4 ZLJN => 7 DMWS
5 KPCF, 1 DLMDJ, 1 FNWGH => 6 TSTF
8 DTWKS, 1 GBDG => 4 CGZQ
26 CNWZM, 4 KPCF => 3 DTWKS
1 JVLHM, 7 DTWKS, 7 PJBZT => 8 MRPHV
2 MWDXJ => 3 VHFPC
1 WXNW, 6 PFKRW => 7 ZVGVP
2 ZVGVP => 1 CMHMQ
8 JVLHM, 11 XRKN, 1 HCGKZ => 8 CHZLX
20 TSTF => 4 XDZMZ
3 CMHMQ, 7 ZVGVP, 10 XRKN => 9 FNWGH
12 HCGKZ, 4 NLSBZ, 15 RWRDP, 4 MRPHV, 31 KRDV, 6 PMXK, 2 NFVZ => 7 KNGJ
1 TXZCM => 9 BMPJ
2 ZFXQ => 3 NBRHT
13 JVLHM, 1 VHFPC => 3 PBJPZ
7 HCGKZ => 7 PMXK
2 RWRDP, 3 VSTQ, 12 PMXK => 7 MXNK
1 PJBZT, 3 QRSK => 1 KRDV
1 MGCKC, 6 CMHMQ => 6 PQTVS
1 TNHCS, 24 ZLJN => 4 RWRDP
5 MWDXJ, 1 WXNW => 9 QBCLF
1 ZFXQ, 1 DLMDJ => 4 DJXRM
1 ZFXQ => 2 CNWZM
1 KPCF => 6 ZXDVF
2 MRPHV => 1 GSTG
5 BMPJ, 2 ZLJN => 8 XQJZ
1 MWDXJ, 1 ZVGVP => 3 CDVNK
3 NFCB, 3 CMHMQ, 1 MWDXJ => 4 XRKN
1 WXNW, 1 TXZCM => 5 ZLJN
4 ZXDVF => 4 WBVJ
2 GBDG => 4 KPCF
4 CHZLX, 7 ZFXQ, 14 PQTVS => 9 VSTQ
3 TXZCM, 7 ZLJN, 7 ZXDVF => 9 JVLHM
1 DMWS, 3 TSTF => 5 HCGKZ
2 CGZQ => 4 NFVZ
2 PQTVS, 9 VMNJ => 9 TXZCM
3 KPCF => 4 DLMDJ
7 VMNJ, 24 XQJZ, 7 GSTG, 8 NLSBZ, 10 MGCKC, 2 SFJFX, 18 BMPJ => 1 NSWK
41 CNWZM, 5 DJXRM, 1 QRSK, 1 KPCF, 15 XDZMZ, 3 MRPHV, 1 NLSBZ, 9 KRDV => 2 WNFSV
10 PBJPZ, 29 BMPJ, 2 PMXK => 7 SFJFX
116 ORE => 4 WXNW
2 CNWZM => 2 TNHCS
10 QBCLF => 7 NFCB
1 QBCLF => 2 ZFXQ
15 ZLJN => 7 QRSK
183 ORE => 3 QDJCL
11 GBDG => 5 VMNJ
4 DMWS, 3 QRSK => 3 NHTKL
124 ORE => 6 VXFRX
1 MWDXJ => 6 MGCKC
108 ORE => 9 PFKRW"""

recipes = rawcookbook.split("\n")
print(recipes)

recipes = [x.split(" => ") for x in recipes]
print(recipes)

recipes = [[y, x.split(", ")] for x, y in recipes]
print(recipes)

cookbook = [(recipe[0].split(" "), [x.split(" ") for x in recipe[1]]) for recipe in recipes]
print(cookbook)

ingredients = [recipe[0][1] for recipe in cookbook]
print(ingredients)

leftovers = {ingredient: 0 for ingredient in ingredients}
print(leftovers)

# exit(0)
ore_1 = produce("FUEL", 1, cookbook, leftovers)

trillion = 1000000000000

fuel_request = math.floor(trillion/ore_1)
ore_1 = ore_1 * fuel_request

xf = (ore_1 - trillion) / trillion

while True:

    leftovers = {ingredient: 0 for ingredient in ingredients}

    ore = produce("FUEL", fuel_request, cookbook, leftovers)
    xf = (ore - trillion) / trillion
    if ore > trillion:
        print(ore - trillion, fuel_request)
        fuel_request =  math.floor( fuel_request * (1-xf) )

    elif ore < trillion:
        print(ore - trillion, fuel_request)
        fuel_request =  math.ceil( fuel_request * (1-xf) )

    else:
        print("jackpot")
        print(fuel_request, fuel_request)
        break



exit(0)


# print( trillion / 2210736 )
# print(460664 - 452338)
