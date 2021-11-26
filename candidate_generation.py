from sklearn.metrics import ndcg_score
from scipy import stats
import numpy as np
import pandas as pd
import gensim as gn
import multiprocessing as mp


def candidate_generation(entity, size, embedding_model,event_ids):
    df_tmp=pd.DataFrame(columns={"id","similars"})
    try:         
        kk=2000
        similars_=[]
        while(len(similars_)<=size):
            similars=embedding_model.most_similar(entity, topn=kk)      
            similars_id=[r[0] for r in similars]
            #### Here we are only choosing those that are events
            similars_=list(set(event_ids)&set(similars_id))
            kk=kk+200
        df_tmp=df_tmp.append({"id":entity, "similars":similars_[:size+1]}, ignore_index=True)
        return(df_tmp)
    except:
        pass

def main(entity,size, event,embedding_model, workers): 
    ##### make sure that the  columns are:
    
    events=pd.read_pickle(event)
    event_ids=list(events["event"].unique())
    event_df=pd.DataFrame(event_ids)
    event_df.columns={"event"}
    embedding_model=gn.models.Word2Vec.load(embedding_model)
    df=candidate_generation(entity, size, embedding_model,event_ids)
    return(df.iloc[0]["similars"])


if __name__=="__main__":
    main()

