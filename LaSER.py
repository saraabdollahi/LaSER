from sklearn.metrics import ndcg_score
from scipy import stats
import numpy as np
import pandas as pd
import gensim as gn
import multiprocessing as mp
from math import sin, cos, sqrt, atan2, radians
import pickle
import xgboost as xgb
import argparse
import candidate_generation
from test import feature_extraction

#### as input we should get language and the query entity

language_interlinks=pd.read_csv("/data/language_interlinks.txt", sep="\t")


def parse_args():
    
   
    parser = argparse.ArgumentParser(description="Event Recommendation")
    parser.add_argument('--query', type=str, default="Kingdom_of_Hungary",
                    help='The query entity you want to see recommended events. Default is "Film_Festival".')
    parser.add_argument('--language', type=str, default="german",
                    help='The language you want to see the recemmended events in. You could choose among german, russian and french.')
    parser.add_argument('--embedding_method', type=str, default="sample_deepwalk",
                    help='Embedding method. Default is node2vec.')
    parser.add_argument('--entities_size', type=int, default=2369967,
                    help='The number of entities in a language.')
    parser.add_argument('--LTR_model', type=str, default="LTR_model",
                    help='The ranking model. Default is LTR_model')

    return parser.parse_args()


def main(args):
    
    query_entity=list(language_interlinks.loc[language_interlinks["english"]==args.query,args.language])[0]
    candidate_dataset=candidate_generation.main(query_entity,100, args.embedding_method)
    features_dataset=feature_extraction(candidate_dataset, args.language,args.embedding_method, args.entities_size)


    with open(args.LTR_model, "rb") as file:
        LTR_model=pickle.load(file)    


    features_dataset["relevance_score"]=1
    data=features_dataset.sort_values(by="source")
    hh=data.groupby("source").size().reset_index(name="size")
    h=hh["size"].values
    target_test=data["relevance_score"]
    x_test=data[["shared_incoming_cnt","shared_outgoing_cnt","embedding_similarity","pair_distance","source_incoming_cnt", "target_incoming_cnt","source_outgoing_cnt","target_outgoing_cnt", "language_distance", "milne_witten","begin_time_distance", "interval_overlap" ]].apply(pd.Series)
    xgtest=xgb.DMatrix(x_test.values, target_test.values)
    xgtest.set_group(h)
    predictions=LTR_model.predict(xgtest)
    data["prediction"]=predictions


    data=data[["source","target","prediction"]]
    label_data=pd.merge(pd.merge(left=data, right=language_interlinks, how="left", left_on="source", right_on=args.language),right=language_interlinks, how="left", left_on="target", right_on=args.language)
    label_data["english_x"]=label_data["english_x"].fillna(label_data["source"])
    label_data["english_y"]=label_data["english_y"].fillna(label_data["target"])
    label_data["rank"]=label_data.groupby("english_x")["prediction"].rank("first", ascending=False)

    label_data=label_data.sort_values(by="rank")
    label_data=label_data.loc[label_data["rank"]<=10,]
    return(list(label_data["english_y"].unique()))


if __name__=="__main__":
    args=parse_args()
    main(args)
#
