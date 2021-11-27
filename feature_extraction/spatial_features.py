import pandas as pd
import numpy as np
from math import sin, cos, sqrt, atan2, radians
import shapefile
import shapely
from shapely.geometry import Point
from shapely.geometry import shape
from pyproj import Proj




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

def pair_distance(input_data):
    ### input_data contains source and target
    coordinates=pd.read_pickle("/data/coordinates_dataset")
    coordinates_data=pd.merge(pd.merge(left=input_data, right=coordinates, how="left", left_on="source", right_on="entity"), right=coordinates, how="left", left_on="target", right_on="entity")
    tmp1=coordinates_data.loc[coordinates_data["coordinates_y"].notna(),]
    tmp2=tmp1.loc[tmp1["coordinates_x"].notna(),]

    coordinates_data["empty_list"]=coordinates_data.apply(lambda row: [], axis=1)
    coordinates_data["coordinates_x"]=coordinates_data["coordinates_x"].fillna(coordinates_data["empty_list"])
    coordinates_data["coordinates_y"]=coordinates_data["coordinates_y"].fillna(coordinates_data["empty_list"])

    coordinates_data["pair_distance"]=-1
    
    del coordinates_data["empty_list"]

    coordinates_data=coordinates_data.reset_index(drop=True)
    for k in range(coordinates_data.shape[0]):
        coordinates_data.loc[k,"pair_distance"]=distance_calculating(coordinates_data.iloc[k]["coordinates_x"], coordinates_data.iloc[k]["coordinates_y"])
    del coordinates_data["coordinates_x"]
    del coordinates_data["coordinates_y"]
    del coordinates_data["entity_x"]
    del coordinates_data["entity_y"]
    return(coordinates_data)

    
   

            
            
def language_distance(input_data,language):
    nys=Proj(init="EPSG:32117")
    events=pd.read_pickle(language+"_events")
    coordinates=pd.read_pickle("sample_coordinates")
    all_coordinates=pd.merge(left=events, right=coordinates, how="left", left_on="event", right_on="entity")
    all_coordinates=all_coordinates[["entity","coordinates"]]
    all_coordinates=all_coordinates.loc[all_coordinates["coordinates"].notna(),]
    all_coordinates=all_coordinates.loc[all_coordinates["entity"].notna(),]
    all_coordinates=all_coordinates.reset_index(drop=True)
    sf=shapefile.Reader("TM_WORLD_BORDERS-0.3.shp",encoding="utf8" ,encodingErrors="replace")
    all_shapes=sf.shapes()
    all_records=sf.records()
    
    countries=pd.read_csv("countries_languages.csv", sep=",")
    countries_list=list(countries.loc[countries["language"]==language,"countryLabel"].unique())
    language_records=[i for i,x in enumerate(all_records) if x[4] in countries_list]
    boundry_list=[]
    for l in range(len(language_records)):
        boundry_list.append(all_shapes[language_records[l]])
    tmp_df=pd.DataFrame(columns={"entity","language_distance"})
 
    all_entities=list(all_coordinates["entity"].unique())
    for k in range(all_coordinates.shape[0]):
        src_coord=all_coordinates.iloc[k]["coordinates"]
        entity=all_coordinates.iloc[k]["entity"]
        distance_tmp=[]
 
        for j in range(0, 20, 2):
            lat1=src_coord[j]
            lon1=src_coord[j+1]

            if (lat1==0) | (lon1==0):
                break
            else:
                distances=[]
                for p in range(len(boundry_list)):
                    p1=Point(lat1, lon1)
                    p1_proj=nys=(p1.y, p1.x)
                    dis=((shape(all_shapes[language_records[p]])).distance(Point(p1_proj)))
                    distances.append(dis)
                
        tmp_df=tmp_df.append({"entity":entity,"language_distance":np.min(distances)},ignore_index=True)

    final_df=pd.merge(left=data, right=tmp_df, how="right", left_on="target", right_on="entity")
    del final_df["entity"]
    return(final_df)

                
