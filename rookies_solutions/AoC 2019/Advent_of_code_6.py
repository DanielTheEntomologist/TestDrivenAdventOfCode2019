import pandas as pd
import easygui
import os
import math
import copy
from pathlib import PureWindowsPath


def realign_map(map, new_center, body, log):
    try:
        # print("visiting", body)
        log_freq = 1
        targets = map.loc[body]['sat']
        # print(targets)
        if isinstance(targets, str):

            # print("departing for single " + str(targets))
            # log.append("departing for " + str(targets) + "\n")
            # if len(log) % log_freq == 0:
            #    print(log[-log_freq:])
            print("going from", body, "to", targets)
            map, token, r_body = realign_map(map, new_center, targets, log)
            print("returning from ", r_body, "to", body,"with" , token)

            if token:
                # flip relation
                # print(body, "is single")
                print("returning to base")
                formal.loc[(formal["center"] == body) & (formal["sat"] == r_body), ['flip']] = True
                #map.loc[body, 'flip'] = True
                # print(map)

                return map, True, body
        else:
            for x in targets:
                # print("departing for " + str(x))
                # log.append("departing for " + str(x) + "\n")
                # if len(log) % log_freq == 0:
                #    print(log[-log_freq:])
                print("going from", body, "to", x)
                map, token, r_body = realign_map(map, new_center, x, log)
                print("returning from ", r_body, "to", body)
                if token:
                    print("Returning to base")
                    #map.loc[body == x]['flip'] = True
                    formal.loc[(formal["center"] == body) & (formal["sat"] == r_body), ['flip']] = True
                    # flip relation and break
                    return map, True, body
                    #break
        return map, False, body

    except KeyError:
        if body == new_center:
            return map, True, body
        else:
            return map, False, body


def explore(map, body, distance, log):
    try:
        # print("visiting", body, "with distance",distance)

        log_freq = 1000
        targets = map.loc[body]['sat']
        #print('visiting',body)
        #print('can go to ', targets)
        if isinstance(targets, str):

            log.append("departing for " + str(targets) + "\n")
            if len(log) % log_freq == 0:
                print(log[-log_freq:])
            explore(map, targets, distance + 1, log)
        else:
            for x in targets:
                log.append("departing for " + str(x) + "\n")
                if len(log) % log_freq == 0:
                    print(log[-log_freq:])
                explore(map, x, distance + 1, log)
        return None

    except KeyError:
        if body == "SAN":
            print("Santa is ",distance-2,"orbital transfers away")
        else:
            return None


map = ['COM)B',
       'B)C',
       'C)D',
       'D)E',
       'E)F',
       'B)G',
       'G)H',
       'D)I',
       'E)J',
       'J)K',
       'K)L']
# relations = [ str.split(x,")") for x in map ]
map_to_santa = ["COM)B",
                "B)C",
                "C)D",
                'D)E',
                'E)F',
                'B)G',
                'G)H',
                'D)I',
                'E)J',
                'J)K',
                'K)L',
                'K)YOU',
                'I)SAN']
# relations_to_santa = [ str.split(x,")") for x in map ]

path = PureWindowsPath(r"C:\Users\boda9003\Desktop\Python_playground\Advent of Code\Inputs\orbitmap_6.csv")
formal = pd.read_csv(path, header=None, sep=";", dtype=str)

#formal = pd.DataFrame(map_to_santa)
formal = formal[0].str.split(")", expand=True)
formal.columns = ['center', 'sat']

formal = formal.set_index(formal['center'])  # .set_index(formal['sat']) #.drop(['center'], axis=1)
formal["flip"] = False

#print(formal)
log = []

#formal.loc[(formal["center"]=="D")&(formal["sat"]=="I"),['flip']] = True
#report.loc[~report['MSR_CEL_ID'].isna(), ["SAMPLE"]] = "yes"

#print(formal)


realignement_chart, flipped, r_body = realign_map(formal, 'YOU', 'COM', log)

realignement_chart ["new_center"] = realignement_chart.apply(lambda x: x['sat'] if x['flip'] else x['center'] ,axis = 1)
realignement_chart ["new_sat"] = realignement_chart.apply(lambda x: x['center'] if x['flip'] else x['sat'] ,axis = 1)
#print(realignement_chart)

map_to_santa = realignement_chart[['new_center','new_sat']].reset_index().drop(columns="center")
map_to_santa.columns = ['center', 'sat']
print(map_to_santa)
map_to_santa.index=map_to_santa["center"].drop(columns="center")
print("MAP TO SANTA:\n",map_to_santa)


# formal = formal.set_index(formal['center']).drop(['center'], axis=1)

log = []
explore(map_to_santa, "YOU", 0, log)

# input("press enter to exit")
