import pandas as pd
from links import link_based_features
from milne_witten import MW_features
from embedding_similarity import embedding_similarity
from spatial_features import language_distance, pair_distance
from temporal_features import temporal_features


def feature_extraction(input_dataset,language,embedding_model, entities_size):

    df1=language_distance(input_dataset, language)
    df2=pair_distance(df1)
    df3=temporal_features(df2)
    df4=link_based_features(df3)
    df5=embedding_similarity(df4, embedding_model)
    features_dataset=MW_features(df5, entities_size)
    print(features_dataset)







