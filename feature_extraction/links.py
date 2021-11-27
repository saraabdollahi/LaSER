import pandas as pd
import numpy as np
import argparse


def link_based_features(input_dataset):
    
    link_graph=pd.read_csv("/data/link_graph.txt", sep="\t")
    all_entities=list(set(list(input_dataset["source"].unique())+list(input_dataset["target"].unique())))
    incoming_tmp=link_graph.loc[link_graph["target"].isin(all_entities),]
    outgoing_tmp=link_graph.loc[link_graph["source"].isin(all_entities),]
    incoming_lists=incoming_tmp.groupby("target")["source"].apply(list).reset_index(name="incoming")
    incoming_lists=incoming_lists.rename(columns={"target":"target_entity"})
    outgoing_lists=outgoing_tmp.groupby("source")["target"].apply(list).reset_index(name="outgoing")
    outgoing_lists=outgoing_lists.rename(columns={"source":"source_entity"})

    merged_links=pd.merge(pd.merge(left=input_dataset, right=incoming_lists, how="left", left_on="source", right_on="target_entity"), right=incoming_lists, how="left", left_on="target", right_on="target_entity")
    
    merged_links=pd.merge(pd.merge(left=merged_links, right=outgoing_lists, how="left", left_on="source", right_on="source_entity"), right=outgoing_lists, how="left", left_on="target", right_on="source_entity")
    merged_links["empty"]=merged_links.apply(lambda row: [], axis=1)
    merged_links["incoming_x"]=merged_links["incoming_x"].fillna(merged_links["empty"])
    merged_links["incoming_y"]=merged_links["incoming_y"].fillna(merged_links["empty"])
    merged_links["outgoing_x"]=merged_links["outgoing_x"].fillna(merged_links["empty"])
    merged_links["outgoing_y"]=merged_links["outgoing_y"].fillna(merged_links["empty"])

    merged_links["shared_incoming_cnt"]=merged_links.apply(lambda row:len(set(row.incoming_x)&set(row.incoming_y)), axis=1)
    merged_links["shared_outgoing_cnt"]=merged_links.apply(lambda row:len(set(row.outgoing_x)&set(row.outgoing_y)), axis=1)
    merged_links["source_incoming_cnt"]=merged_links.apply(lambda row:len(row.incoming_x), axis=1)
    merged_links["target_incoming_cnt"]=merged_links.apply(lambda row:len(row.incoming_y), axis=1)
    merged_links["source_outgoing_cnt"]=merged_links.apply(lambda row:len(row.outgoing_x), axis=1)
    merged_links["target_outgoing_cnt"]=merged_links.apply(lambda row:len(row.outgoing_y), axis=1)
    del merged_links["empty"]
    del merged_links["incoming_x"]
    del merged_links["incoming_y"]
    del merged_links["outgoing_x"]
    del merged_links["outgoing_y"]
    del merged_links["source_entity_x"]
    del merged_links["source_entity_y"]
    del merged_links["target_entity_x"]
    del merged_links["target_entity_y"]
    
    

    return(merged_links)

    




