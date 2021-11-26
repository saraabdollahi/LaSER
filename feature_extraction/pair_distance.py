import pandas as pd
import numpy as np
from math import sin, cos, sqrt, atan2, radians



#approximate radius of earth in km

def distance_calculating(source_coordinates, target_coordinates):
    R=6373.0
    distance_list=[]    
    if not source_coordinates: 
        distance=-1
    elif not target_coordinates:
        distance=-1
    else:
        for j in range(0, 20, 2):                       
            lat1=float(source_coordinates[j])
            lon1=float(source_coordinates[j+1])
            lat2=float(target_coordinates[j])
            lon2=float(target_coordinates[j+1])

            if (lat1==0) | (lat2==0):
                distance_list.append(-1)
            else:
                dlon=lon2-lon1
                dlat=lat2-lat1
                a=sin(dlat/2)**2+cos(lat1)*cos(lat2)*sin(dlon/2)**2
                c=2*atan2(sqrt(a),sqrt(1-a))
                tmp_distance=R*c
                distance_list.append(tmp_distance)
        l=[x for x in distance_list if x!=-1]
        if l:
            distance=min(l)
            return(distance)

def main(input_data):
    ### input_data contains source and target
    #coordinates=pd.read_csv(args.coordinates_address, sep="\t") ### contains wikidata_id, coordinates
    input_data=pd.read_pickle(input_data)
    coordinates=pd.read_pickle("sample_coordinates")
    coordinates_data=pd.merge(pd.merge(left=input_data, right=coordinates, how="left", left_on="source", right_on="entity"), right=coordinates, how="left", left_on="target", right_on="entity")
    tmp1=coordinates_data.loc[coordinates_data["coordinates_y"].notna(),]
    tmp2=tmp1.loc[tmp1["coordinates_x"].notna(),]
    print(tmp2)

    coordinates_data["empty_list"]=coordinates_data.apply(lambda row: [], axis=1)
    coordinates_data["coordinates_x"]=coordinates_data["coordinates_x"].fillna(coordinates_data["empty_list"])
    coordinates_data["coordinates_y"]=coordinates_data["coordinates_y"].fillna(coordinates_data["empty_list"])
    print(coordinates_data.loc[coordinates_data["coordinates_y"].notna(),])

    coordinates_data["distance"]=-1
    print(coordinates_data.columns)
    
    del coordinates_data["empty_list"]

    coordinates_data=coordinates_data.reset_index(drop=True)
    for k in range(coordinates_data.shape[0]):
        coordinates_data.loc[k,"distance"]=distance_calculating(coordinates_data.iloc[k]["coordinates_x"], coordinates_data.iloc[k]["coordinates_y"])
        #print(data.columns)
    del coordinates_data["coordinates_x"]
    del coordinates_data["coordinates_y"]
    del coordinates_data["entity_x"]
    del coordinates_data["entity_y"]
    return(coordinates_data)

    
   
   
