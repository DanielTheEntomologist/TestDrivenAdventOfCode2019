# import pandas as pd
# import easygui
# import os
import math

# import copy
# from pathlib import PureWindowsPath
# from collections import deque
# from collections import defaultdict
# from collections import Counter
# import matplotlib
# import matplotlib.pyplot as plt
# import numpy as np

def next_i_sign(i):
    # j = i+1
    j = 0
    k = i-1
    z = 1
    patt = [0, 1, 0, -1]
    while True:
        while z < 4:
            while j < i:
                yield j+k,patt[z]
                j += 1
            k+=j*2
            j = 0
            z += 2
        z = 1

    # while num < n:
    #    yield num
    # num += 1



# gen1 = next_i_sign(1)
#
#
# for x in range(12):
#     print(next(gen1))
#
# del gen1
# exit(0)

message_str = "59773775883217736423759431065821647306353420453506194937477909478357279250527959717515453593953697526882172199401149893789300695782513381578519607082690498042922082853622468730359031443128253024761190886248093463388723595869794965934425375464188783095560858698959059899665146868388800302242666479679987279787144346712262803568907779621609528347260035619258134850854741360515089631116920328622677237196915348865412336221562817250057035898092525020837239100456855355496177944747496249192354750965666437121797601987523473707071258599440525572142300549600825381432815592726865051526418740875442413571535945830954724825314675166862626566783107780527347044"

#message_str = "80871224585914546619083218645595"

#solving 2nd part with halfscrambled message
message_offset = 5977377
message_str = message_str*10000

l = len(message_str)

message_rev = message_str[-1::-1]
message_rev_half = message_rev[0:int(l/2)]

message_rev_half = [int(char) for char in message_rev_half]

half_rev_copy = message_rev_half.copy()

k = 0
while k<100:
    count = 0
    for i,x in enumerate(message_rev_half):
        count += x
        #print(x)
        #print(count)
        count = count % 10
        half_rev_copy[i]=count
    message_rev_half = half_rev_copy

    k+=1
    print(k)
#print("A",half_copy*2)

half_copy = half_rev_copy[-1::-1]


meaning = half_copy[message_offset-len(half_copy):message_offset-len(half_copy)+8]

final = "".join([str(x) for x in meaning])
print("message is:", final)

exit(0)
#message = [1, 2, 3, 4, 5, 6, 7, 8]

 #*10000

#message_str = "80871224585914546619083218645595"
message = [int(char) for char in message_str]
leng = len(message)
message_buffer = message.copy()
k = 0
#print(k,message_buffer)
while k < 100:
    for i in range(leng):
        # prepare pattern
        temp_gen = next_i_sign(i+1)
        count = 0
        try:
            while True:
                adr, sign = next(temp_gen)
                count = count + sign * message_buffer[adr]
        except IndexError:
            message_buffer[i] = int(str(count)[-1])

    k += 1

print("M",message_buffer)

diff = [x-y for x,y in zip(half_copy*2,message_buffer)]

print("D",diff)
#print(k, message)

# #########################################
exit(0)

message_str = "59773775883217736423759431065821647306353420453506194937477909478357279250527959717515453593953697526882172199401149893789300695782513381578519607082690498042922082853622468730359031443128253024761190886248093463388723595869794965934425375464188783095560858698959059899665146868388800302242666479679987279787144346712262803568907779621609528347260035619258134850854741360515089631116920328622677237196915348865412336221562817250057035898092525020837239100456855355496177944747496249192354750965666437121797601987523473707071258599440525572142300549600825381432815592726865051526418740875442413571535945830954724825314675166862626566783107780527347044"

message = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1]

new_message = message.copy()

for i in range(len(message)):
    pass

# message = [int(char) for char in message_str] #*10000
pattern = [0, 1, 0, -1]
# rpattern = pattern[-1::-1]

# print(rpattern)

leng = len(message)
x = math.ceil(leng / len(pattern))

message_buffer = message.copy()

k = 0
print(k, message)

while k < 100:
    for i in range(leng):
        # prepare pattern
        rlpattern = [p for p in pattern for z in range(i + 1)]
        # print(rlpattern)
        # print(x)
        if len(rlpattern) <= leng:
            rlpattern = rlpattern * (x + 1)
        #   print(rlpattern*x)
        rlpattern = rlpattern[1: (leng + 1)]
        # print(len(rlpattern))
        # print(rlpattern)

        message_buffer[i] = sum([m * p for m, p in zip(message, rlpattern)])

        message = [int(str(m)[-1]) for m in message_buffer]
    k += 1
    print(k, message)
