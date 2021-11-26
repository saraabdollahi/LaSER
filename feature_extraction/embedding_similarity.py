import numpy as np
import pandas as pd
import gensim as gn

def embedding_similarity(x, embedding_model):
    #### model chooses between deepwalk and node2vec embedding models
   # model=gn.models.Word2Vec.load(model)
    dataframe=pd.read_pickle(x)
    model=gn.models.Word2Vec.load(embedding_model)
 
    dataframe["embedding_similarity"]=0.0
    for i in range(dataframe.shape[0]):
        try:
            source=dataframe.iloc[i]["target"]
            target=dataframe.iloc[i]["source"]
            sim=model.similarity((source), (target))
            dataframe.loc[i,"embedding_similarity"]=sim
        except:
            dataframe.loc[i,"embedding_similarity"]=np.nan
 
    return (dataframe)
