import pandas as pd
import numpy as np


def start_diff(t1, t2):
    try:
        return((t1-t2).days)
    except:
        return(np.nan)

def min_date(t1,t2):
    try:
        return(min(t1,t2))
    except:
        return(np.nan)

def max_date(t1, t2):
    try:
        return(max(t1,t2))
    except:
        return(np.nan)

def overlapping(t1,t2):
    try:
        return((t2-t1).days)
    except:
        return(np.nan)


def temporal_features(input_data):
    entities_dates=pd.read_pickle("/data/temporal_dataset")
    temporal_dataframe=pd.merge(pd.merge(left=input_data, right=entities_dates, how="left", left_on="source", right_on="entity"), right=entities_dates, how="left", left_on="target", right_on="entity")
    temporal_dataframe["start_diff"]=temporal_dataframe.apply(lambda row: start_diff(row.start_date_x,row.start_date_y), axis=1)
    temporal_dataframe["max_start"]=temporal_dataframe.apply(lambda row: max_date(row.start_date_x,row.start_date_y), axis=1)
    temporal_dataframe["min_end"]=temporal_dataframe.apply(lambda row: min_date(row.end_date_x,row.end_date_y), axis=1)
    temporal_dataframe["interval_overlap"]=temporal_dataframe.apply(lambda row: overlapping(row.max_start,row.min_end), axis=1)
    temporal_dataframe["begin_time_distance"]=temporal_dataframe["start_diff"].abs()
    del temporal_dataframe["max_start"]
    del temporal_dataframe["min_end"]
    del temporal_dataframe["start_diff"]
    del temporal_dataframe["entity_x"]
    del temporal_dataframe["entity_y"]
    del temporal_dataframe["start_date_x"]
    del temporal_dataframe["start_date_y"]
    del temporal_dataframe["end_date_x"]
    del temporal_dataframe["end_date_y"]
    return(temporal_dataframe)
