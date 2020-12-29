#!/usr/local/bin/python3
#
# route.py : Find Directon from one city to Another
#
# Submitted by : Group
#
#
#

from IPython.display import display, HTML
from pprint import pformat
import math
import sys
import pandas as pd
import urllib
import pickle
from pandas import DataFrame
from queue import PriorityQueue
fringe = PriorityQueue(maxsize=0)
#tmp_fringe =

def boxprint(*args):
    for arg in args:
        display(HTML('<pre style="white-space: pre !important;">{}</pre>'.format(pformat(arg))))

def open_city_gps():
    city_gps_org=pd.read_csv("/u/purama/city-gps.txt", delimiter=' ')
    return city_gps_org

def city_freeway(starting_city,final_city):
    road_segment=pd.read_csv("/u/purama/road-segments.txt", delimiter=' ')
    road_segment["FIRST_CITY_NM"]= road_segment["FIRST_CITY"].str.split(',_').str[0]
    road_segment["FIRST_STATE"]= road_segment["FIRST_CITY"].str.split(',_').str[1]
    road_segment["SECOND_CITY_NM"]= road_segment["SECOND_CITY"].str.split(',_').str[0]
    road_segment["SECOND_STATE"]= road_segment["SECOND_CITY"].str.split(',_').str[1]
    road_segment["CITY_PATH"]= ""
    #print (road_segment)
    city_gps=Distance_to_final_city(starting_city,final_city)
    #city_gps=pd.read_csv("/Volumes/Macintosh HD - Data/Purushoth/IU/Course/ElementsOf_AI/jamcshan-samize-purama-a1-master/part2/city-gps.txt", delimiter=' ')
    road_segment_gps=pd.merge(road_segment, city_gps, left_on="FIRST_CITY", right_on="CITY", how='left').rename(columns={"LATITUDE": "FIRST_LATITUDE", "LOGINTUDE": "FIRST_LOGINTUDE", "DISTANCE_FRM_STRT_STATE": "FIRST_CITY_DISTANCE_FRM_STRT", "DISTANCE_TO_GOAL_STATE": "FIRST_CITY_DISTANCE_TO_GOAL"}).drop(columns={"CITY"})
    road_segment_gps2=pd.merge(road_segment_gps, city_gps, left_on="SECOND_CITY", right_on="CITY", how='left').rename(columns={"LATITUDE": "SECOND_LATITUDE", "LOGINTUDE": "SECOND_LOGINTUDE","DISTANCE_FRM_STRT_STATE": "SECOND_CITY_DISTANCE_FRM_STRT",  "DISTANCE_TO_GOAL_STATE": "SECOND_CITY_DISTANCE_TO_GOAL"}).drop(columns={"CITY"})
    #road_segment_gps2["DIFF_LAT"]=road_segment_gps2["FIRST_LATITUDE"]-road_segment_gps2["SECOND_LATITUDE"]
    #print (road_segment_gps2)

    return road_segment_gps2

def Distance_to_final_city (starting_city,final_city):

    city_gps=open_city_gps()
    l_final_city_coordinates=city_gps[city_gps[('CITY')].str.lower()==(final_city).lower()].values.tolist()
    l_stating_city_coordinates=city_gps[city_gps[('CITY')].str.lower()==(starting_city).lower()].values.tolist()

    for i in range(len(city_gps)) :

        #print (type(city_gps))
        l_other_city_coordinates=[city_gps.loc[i, "CITY"], city_gps.loc[i, "LATITUDE"], city_gps.loc[i, "LOGINTUDE"]]
        #print(l_final_city_coordinates)
        #print (len(l_final_city_coordinates))

        R = 6373.0 #Km

        lat1 = math.radians(l_other_city_coordinates[1])
        lon1 = math.radians(l_other_city_coordinates[2])
        lat2 = math.radians(l_final_city_coordinates[0][1])
        lon2 = math.radians(l_final_city_coordinates[0][2])
        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c * 0.62137119224     #Miles

        city_gps.loc[i, "DISTANCE_TO_GOAL_STATE"] = distance
        #print (city_gps.loc[i])

        # Find Distance from Starting State
        lat2 = math.radians(l_stating_city_coordinates[0][1])
        lon2 = math.radians(l_stating_city_coordinates[0][2])
        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c * 0.62137119224     #Miles

        city_gps.loc[i, "DISTANCE_FRM_STRT_STATE"] = distance

    #print (city_gps)
    return city_gps

def next_state (src_df, l_src_fringe, l_f_visited_fringe):

     # Convert visited state list to dataframe.
    df_visited_fringe = DataFrame (l_f_visited_fringe,columns=['V_CITY','V_RD'])
    #print ("Visited DF")
    #print (df_visited_fringe)

    # Next City from First City.
    src_df_1=src_df[(src_df[('RD')]==l_src_fringe[3]) & ((src_df[('FIRST_CITY_DISTANCE_FRM_STRT')].mask(pd.isnull, 0))>l_src_fringe[1]) ]
    src_df_1['RNK']=src_df_1['FIRST_CITY_DISTANCE_FRM_STRT'].rank(method='dense')
    src_df_2=src_df_1[src_df_1['RNK']==1]
    src_df_2['CITY_PATH']= l_src_fringe[4] + '~' + src_df_2['FIRST_CITY']

    # Eliminate the city which is already available in Visited State -- From First City
    src_df_first_city = src_df_2.merge(df_visited_fringe, how='left', left_on=["FIRST_CITY","RD"], right_on=["V_CITY","V_RD"])
    src_df_first_city_fnl = src_df_first_city[(src_df_first_city[('V_CITY')].isnull())]
    src_df_first_city_fnl["J_FIRST_CITY"]=src_df_first_city_fnl["FIRST_CITY"]
    #print ("MergedDataFrame")
    #print (src_df_first_city1)

    l_second_city=src_df_2['SECOND_CITY'].values.tolist()

    src_df_secnd_city_fnl = pd.DataFrame()
    if len(l_second_city) != 0:

        src_df_secnd_city = src_df[(src_df[('RD')] != l_src_fringe[3]) & (src_df[('FIRST_CITY')] == l_second_city[0]) ]

        # Eliminate the city which is already available in Visited State -- From Second City
        src_df_secnd_city_1 = src_df_secnd_city.merge(df_visited_fringe, how='left', left_on=["FIRST_CITY","RD"], right_on=["V_CITY","V_RD"])
        src_df_secnd_city_2 = src_df_secnd_city_1[(src_df_secnd_city_1[('V_CITY')].isnull())]
        src_df_secnd_city_2 = src_df_secnd_city_2.drop(columns=['V_CITY', 'V_RD'])
        src_df_secnd_city_3 = src_df_secnd_city_2.merge(src_df_first_city_fnl, how='left', left_on=["FIRST_CITY","RD"], right_on=["J_FIRST_CITY","RD"])
        src_df_secnd_city_fnl = src_df_secnd_city_3[(src_df_secnd_city_3[('J_FIRST_CITY')].isnull())]
        src_df_secnd_city_fnl =  src_df_secnd_city_fnl.drop(columns=["FIRST_CITY_y", "SECOND_CITY_y", "DIST_y", "SPEED_LIMIT_y", "FIRST_CITY_NM_y", "FIRST_STATE_y", "SECOND_CITY_NM_y", "SECOND_STATE_y", "CITY_PATH_y", "FIRST_LATITUDE_y", "FIRST_LOGINTUDE_y", "FIRST_CITY_DISTANCE_TO_GOAL_y", "FIRST_CITY_DISTANCE_FRM_STRT_y", "SECOND_LATITUDE_y", "SECOND_LOGINTUDE_y", "SECOND_CITY_DISTANCE_TO_GOAL_y", "SECOND_CITY_DISTANCE_FRM_STRT_y", "RNK", "J_FIRST_CITY"]).drop_duplicates()
        src_df_secnd_city_fnl['CITY_PATH_x']= l_src_fringe[4] + '~' + src_df_secnd_city_fnl['FIRST_CITY_x']


    l_src_df_first_city_fnl=[]
    for i, row in src_df_first_city_fnl.iterrows():
        l_src_df_first_city_fnl= [src_df_first_city_fnl.loc[i, "FIRST_CITY_DISTANCE_TO_GOAL"],src_df_first_city_fnl.loc[i, "FIRST_CITY_DISTANCE_FRM_STRT"] ,src_df_first_city_fnl.loc[i, "FIRST_CITY"], src_df_first_city_fnl.loc[i, "RD"], src_df_first_city_fnl.loc[i, "CITY_PATH"]]

    l_src_df_first_city_fnl1=l_src_df_first_city_fnl
    j=0
    l_src_df_secnd_city_fnl=[]
    ind=0

    if src_df_secnd_city_fnl.empty:
        #print ("No Second City")
        pass
    else:
        for i, row in src_df_secnd_city_fnl.iterrows():
            #print ("i", i)
            if j == 0:
                tmp1=[src_df_secnd_city_fnl.loc[i, "FIRST_CITY_DISTANCE_TO_GOAL_x"],src_df_secnd_city_fnl.loc[i, "FIRST_CITY_DISTANCE_FRM_STRT_x"] ,src_df_secnd_city_fnl.loc[i, "FIRST_CITY_x"], src_df_secnd_city_fnl.loc[i, "RD"], src_df_secnd_city_fnl.loc[i, "CITY_PATH_x"]]
                #print ("tmp")
                #print (tmp1)
                l_tmp=tmp1
                l_src_df_first_city_fnl1=[l_src_df_first_city_fnl]
                l_src_df_first_city_fnl1.append(l_tmp)
                ind=1
            else:
                tmp=[src_df_secnd_city_fnl.loc[i, "FIRST_CITY_DISTANCE_TO_GOAL_x"],src_df_secnd_city_fnl.loc[i, "FIRST_CITY_DISTANCE_FRM_STRT_x"] ,src_df_secnd_city_fnl.loc[i, "FIRST_CITY_x"], src_df_secnd_city_fnl.loc[i, "RD"], src_df_secnd_city_fnl.loc[i, "CITY_PATH_x"]]
                l_tmp=tmp
                l_src_df_first_city_fnl1.append(l_tmp)
            j=j+1
        #tmp_fringe

    #print (l_src_df_first_city_fnl)

    #if len(src_df_secnd_city_fnl) == 0:
    #    print ("List is Empty")

    #else:
        #print ("Consolidated List")
        #print (l_src_df_secnd_city_fnl)

     #   rtn_val=[]
     #   rtn_val.append(l_src_df_first_city_fnl)
     #   rtn_val.append(l_src_df_secnd_city_fnl)
     #   return (rtn_val)


    #l_src_df=(src_df_2['FIRST_CITY_DISTANCE_TO_GOAL'],src_df_2['FIRST_CITY_DISTANCE_FRM_STRT'] ,src_df_2['FIRST_CITY'], src_df_2['RD'], src_df_2['CITY_PATH'])
    #print (l_src_df)


    if ind == 0:
        #print ("No Second City")
        #print (([l_src_df_first_city_fnl1]))
        return ([l_src_df_first_city_fnl1])
    else:
        #print ("With Seconf City")
        #print (l_src_df_first_city_fnl1)
        return (l_src_df_first_city_fnl1)


def solve(first_city, final_city, place_holder):
    pd_df1=city_freeway(first_city, final_city)
    #print (pd_df1)

    pd_df=pd_df1[pd_df1[('FIRST_CITY')].str.lower()==(first_city)]
    #print (pd_df)

    l_visited_fringe =[]
    for i, row in pd_df.iterrows():
        l_pd_df=[pd_df.loc[i, "FIRST_CITY_DISTANCE_TO_GOAL"],pd_df.loc[i, "FIRST_CITY_DISTANCE_FRM_STRT"] ,pd_df.loc[i, "FIRST_CITY"], pd_df.loc[i, "RD"], pd_df.loc[i, "CITY_PATH"]]
        #print (type(l_pd_df))
        fringe.put(l_pd_df)

        l_visited_fringe.append(l_pd_df[2:4])

    #print ("Visted List")
    #print (l_visited_fringe)

    while fringe:

        #print(fringe.get())
        print ("In While Loop")

        print ("Total Fringe")
        print (fringe)

        l_fringe = fringe.get()

        print ("Out From Fringe")
        print (l_fringe)
        l_nxt_state = next_state (pd_df1, l_fringe, l_visited_fringe)
        print ("From Next State Function")
        print ("Length:", len(l_nxt_state))
        print (l_nxt_state)

        if len(l_nxt_state) <= 1:
            pass

        else:

            for lst in l_nxt_state:
                if lst[2]==final_city:
                    print ("Goal Reached")
                    return lst[4]

                fringe.put(lst)
                l_visited_fringe.append(lst[2:4])

        print (fringe.qsize())

        ## Append to Fringe and to Visited List

        if fringe.qsize() == 0:
            print ("No Match")
            return False

    print ("Control Reached exit")
    return False

if __name__ == "__main__":

        s_city=sys.argv[1]
        f_city=sys.argv[2]
        cost=sys.argv[3]
        starting_city=s_city

        final_city=f_city
    pd_df=solve(starting_city.lower(),final_city , 0)
    print (pd_df)
