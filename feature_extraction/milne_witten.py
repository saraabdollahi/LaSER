import pandas as pd
import numpy as np



def main(input_address,link_graph,entities_size):
    
    ### The input_dataset contains two columns: source and target for which we want to compute Milne_Witten score
    input_dataset=pd.read_pickle(input_address)
 
    #### The link_graph contains two columns: entity and links
    link_graph=pd.read_pickle(link_graph)   
    all_entities=list(set(list(input_dataset["source"].unique())+list(input_dataset["target"].unique())))
    incoming_tmp=link_graph.loc[link_graph["target"].isin(all_entities),]
    incoming_lists=incoming_tmp.groupby("target")["source"].apply(list).reset_index(name="incoming")
    incoming_lists=incoming_lists.rename(columns={"target":"target_entity"})

    merged_links=pd.merge(pd.merge(left=input_dataset, right=incoming_lists, how="left", left_on="source", right_on="target_entity"), right=incoming_lists, how="left", left_on="target", right_on="target_entity")
    merged_links["empty"]=merged_links.apply(lambda row: [], axis=1)
    merged_links["incoming_x"]=merged_links["incoming_x"].fillna(merged_links["empty"])
    merged_links["incoming_y"]=merged_links["incoming_y"].fillna(merged_links["empty"])
   
    merged_links["incoming_len_x"]=merged_links.apply(lambda row:len(row.incoming_x), axis=1)
    merged_links["incoming_len_y"]=merged_links.apply(lambda row:len(row.incoming_y), axis=1)
    merged_links["shared_in"]=merged_links.apply(lambda row:len(set(row.incoming_x)&set(row.incoming_y)), axis=1)
    merged_links["min_"]=merged_links[["incoming_len_x","incoming_len_y"]].min(axis=1)
    merged_links["max_"]=merged_links[["incoming_len_x","incoming_len_y"]].max(axis=1)
    merged_links["intersection_log"]=np.log(merged_links.shared_in)
    merged_links["min_log"]=np.log(merged_links.min_)
    merged_links["max_log"]=np.log(merged_links.max_)
    merged_links["w"]=np.log(entities_size)
    merged_links["mw"]=merged_links.apply(lambda row:(row.max_log-row.intersection_log)/(row.w-row.min_log), axis=1)
    merged_links=merged_links.replace([np.inf, -np.inf],0)
    merged_links["milne_witten"]=merged_links.apply(lambda row: 0 if (row.shared_in==0 or row.mw==0) else 1-row.mw, axis=1)
    
    unneeded_columns=["empty","incoming_x","incoming_y","incoming_len_x","incoming_len_y","shared_in","min_","max_","intersection_log","min_log","max_log","w","mw","target_entity_x", "target_entity_y"]
    for k in range(len(unneeded_columns)):
        del merged_links[unneeded_columns[k]]
    #merged_links.to_pickle("MW_tmp")
    return(merged_links)

if __name__=="__main__":
    args = parse_args()
    main(args)    
