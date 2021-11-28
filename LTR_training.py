import multiprocessing as mp
import joblib
import xgboost as xgb
import pandas as pd
from sklearn.metrics import ndcg_score
import numpy as np
from scipy.stats import kendalltau
import random
from sklearn.metrics import mean_squared_error
import warnings
from pandas.core.common import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
from sklearn import preprocessing
import pickle
#from feature_extraction import feature_extraction


data=pd.read_csv("training_dataset.txt", sep="\t")

data=data.loc[data["source"].notna(),]
data=data.reset_index(drop=True)


############# normalizing features
data.loc[data["begin_time_distance"]==-1,"begin_time_distance"]=np.nan
data["begin_time_distance"]=data["begin_time_distance"].abs()
data["interval_overlap"]=data["interval_overlap"]/365
data["begin_time_distance"]=data["begin_time_distance"]/365
data.loc[data["pair_distance"]==-1,"pair_distance"]=np.nan
data.loc[data["language_distance"]==-1,"language_distance"]=np.nan
data["relevance_score"]=data["relevance_score"].fillna(0)
data["shared_incoming_cnt"]=np.log(data["shared_incoming_cnt"])
data["shared_outgoing_cnt"]=np.log(data["shared_outgoing_cnt"])
data["source_incoming_cnt"]=np.log(data["source_incoming_cnt"])
data["target_incoming_cnt"]=np.log(data["target_incoming_cnt"])
data["source_outgoing_cnt"]=np.log(data["source_outgoing_cnt"])
data["target_outgoing_cnt"]=np.log(data["target_outgoing_cnt"])


data=data.replace([np.inf, -np.inf],0)

##### splitting train and test dataset
all_sources=list(data["source"].unique())
interval=int(len(all_sources)/5)
test_sources=all_sources[:interval]
training_sources=list(set(all_sources)-set(test_sources))    

training_data=data.loc[data["source"].isin(training_sources),]
training_data=training_data.reset_index(drop=True)
training_data=training_data.sort_values(by="source")

test_data=data.loc[data["source"].isin(test_sources),]
test_data=test_data.sort_values(by="source")

gg=training_data.groupby("source").size().reset_index(name="size")
g=gg["size"].values

x_train=training_data[["shared_incoming_cnt","shared_outgoing_cnt","embedding_similarity","pair_distance","source_incoming_cnt", "target_incoming_cnt","source_outgoing_cnt","target_outgoing_cnt", "language_distance", "milne_witten","begin_time_distance", "interval_overlap" ]].apply(pd.Series)
y_train_=training_data[["relevance_score"]]

hh=test_data.groupby("source").size().reset_index(name="size")
h=hh["size"].values

x_test=test_data[["shared_incoming_cnt","shared_outgoing_cnt","embedding_similarity","pair_distance","source_incoming_cnt", "target_incoming_cnt","source_outgoing_cnt","target_outgoing_cnt", "language_distance", "milne_witten","begin_time_distance", "interval_overlap" ]].apply(pd.Series)
y_test=test_data[["relevance_score"]]
target_train=training_data["relevance_score"]
target_test=test_data["relevance_score"]

xgtrain=xgb.DMatrix(x_train.values, target_train.values)
xgtrain.set_group(g)
xgtest=xgb.DMatrix(x_test.values, target_test.values)
xgtest.set_group(h)

param={"max_depth":6,"learning_rate":0.9,"booster":"dart","n_jobs":0, "gamma":1.5,"min_child_weight":0.2,"n_estimators":20, "eta":0.1, "objective":"rank:ndcg"}
bst=xgb.train(param, xgtrain) 
file_name="LTR_model"
    
    
model=xgb.train(param, xgtrain) 
file_name="de_LTR_model"
pickle.dump(model, open(file_name, "wb"))

    


