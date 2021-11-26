import pandas as pd
import numpy as np
import multiprocessing as mp
from math import sin, cos, sqrt, atan2, radians
import shapefile
import shapely
from shapely.geometry import Point
from shapely.geometry import shape
from pyproj import Proj
import argparse


            
            
def main(language, coordinates_data):
    nys=Proj(init="EPSG:32117")
    events=pd.read_pickle(language+"_events")
    
    ############# make it consistent across all scripts
    coordinates=pd.read_pickle(coordinates_data)
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
    final_df=pd.DataFrame(columns={})
    all_entities=list(all_coordinates["entity"].unique())
    print(all_coordinates)
    for k in range(all_coordinates.shape[0]):
        print(k)
        src_coord=all_coordinates.iloc[k]["coordinates"]
        entity=all_coordinates.iloc[k]["entity"]
        tmp_df=pd.DataFrame(columns={"entity","polygon_distance"})
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
                
                tmp_df=tmp_df.append({"entity":entity,"polygon_distance":np.min(distances)},ignore_index=True)
    return(tmp_df)


