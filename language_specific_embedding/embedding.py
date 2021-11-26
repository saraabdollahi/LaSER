##### the algorithm
import networkx as nx
import pandas as pd
from numpy.random import choice
import multiprocessing as mp
from multiprocessing import Process
import numpy as np
import gensim as gn
import nltk
import argparse


def parse_args():
    
    ##Parses the Embedding arguments.
   
    parser = argparse.ArgumentParser(description="Embedding")
    
    parser.add_argument('--edgelist', type=str, default="edgelist",
                    help='The address of input edgelist. Default is edgelist.')

    parser.add_argument('--method', type=str, default="node2vec",
                    help='Embedding method. Default is node2vec.')
    
    parser.add_argument('--walks', type=int, default=1,
                    help='Number of Random Walks. Default is 1.')
    
    parser.add_argument('--length', type=int, default=5,
                    help='Length of Random Walks. Default is 5.')
    
    parser.add_argument('--p', type=int, default=4,
                    help='P of Node2Vec. Default is 4.')
    
    parser.add_argument('--q', type=int, default=0.5,
                    help='Q of Node2Vec. Default is 0.5.')
    
    parser.add_argument('--walks_output', type=str, default="generated_walks",
                    help='The address of generated random walks. Default is generated_walks.')
    
    parser.add_argument('--embedding_output', type=str, default="word2vec_model",
                    help='The address of embedding results. Default is word2vec_node2vec.')
    
    parser.add_argument('--workers', type=int, default=15,
                    help='The number of workers for probability_computing, embedding method and word2vec. Default is 15.')
    
    
    
    ###### Word2vec arguments
    
    parser.add_argument('--size', type=int, default=128,
                    help='Size is the size of final vectors. Default is 128.')
    parser.add_argument('--window', type=int, default=3,
                    help='Window size in Word2Vec method. Default is 10.')
   

    return parser.parse_args()



##### for multi-processing
### a shared memory which is the graph and each process access it
### each process generate a walk



##### This function modifies edge weights for node2vec embedding method

def probability_computing(source_node):
    try:    
        ### p=4 and q=0.5
        for current_node in G.neighbors(source_node):
            probs_=list()
            for destination in G.neighbors(current_node):
                if source_node==destination:
                    prob_=G[current_node][destination]["edge"]*(1/args.p)
                elif destination in G.neighbors(source_node):
                    prob_=G[current_node][destination]["edge"]
                else:
                    prob_=G[current_node][destination]["edge"]*(1/args.q)
               
                G[current_node][destination]["edge"]=prob_
       
        return
    except:
        pass
            

##### Sampling strategy for deepwalk method. It randomly choose next node to visit in random walk.        
        
def deepwalk_sampling_strategy(node):
    ff=G[node]
    key=list(ff.keys())
    return (random.sample(key, 1)[0])


##### Sampling strategy for node2vec method. It randomly choose next node to visit in random walk with respect to nodes edges.     

def node2vec_sampling_strategy(node):
 
    ff=G[node]   
    key=list(ff.keys())
    edges=[]
    for i in range(len(ff.keys())):
        edges.append(ff[key[i]]["edge"])
    draw = choice(key, 1, edges)
    return (draw[0])

#normalize the weights



##### The function which generates random walk based on deepwalk method

def deepwalk_generate_walk(node):
        walk=""+str(node)
        walk_list=[]
        walk_list.append(str(node))
        try:
            while len(walk_list)<args.length:
                gg=deepwalk_sampling_strategy(walk_list[-1])
                walk_list.append(gg)
                walk=walk+" "+str(gg)
            return(pd.DataFrane([walk]))
            
        except:
            return (pd.DataFrame([walk]))
    

##### The function which generates random walk based on node2vec method    

def node2vec_generate_walk(node):
        walk=""+str(node)
        walk_list=[]
        walk_list.append(str(node))
        try:
            while len(walk_list)<args.length:
                gg=node2vec_sampling_strategy(walk_list[-1])
                walk_list.append(gg)
                walk=walk+" "+str(gg)
            return(pd.DataFrane([walk]))
            
        except:
            return (pd.DataFrame([walk]))


        
        
def main(args):
    
    
    ##### make sure that the edgelist columns are:
    ##### node1, node2 and edge and convert nodes to string 
    
    edgelist=pd.read_pickle(args.edgelist)
    
    
    
    #### add another argument deciding on the directed or undirected graph
    if(args.method=="node2vec"):
        
        G=nx.from_pandas_edgelist(edgelist, "node1", "node2", edge_attr="edge", create_using=nx.DiGraph())
        
    if(args.method=="deepwalk"):
        G=nx.from_pandas_edgelist(edgelist, "node1", "node2", create_using=nx.DiGraph())
        
    g_nodes=list(G.nodes())
    print("The number of nodes of the graph is: ",len(g_nodes))
     

 #### If the node2vec method is chosen, then the edge weights should be modified by P and Q parameters first
    
    if(args.method=="node2vec"): 
        pool=mp.Pool(args.workers)
        pool.map(probability_computing,g_nodes)
        pool.close() 
        pool.join()
        print("The edges weights are modified for the Node2Vec embedding method.")
    
 

 #### Generating random walks in parallel
    
    walk_df=pd.DataFrame()
    for i in range(args.walks): 
        print("The walk number {} is starting".format(i))
        pool=mp.Pool(args.workers)
        if(args.method=="node2vec"):
            print("Node2vec Embedding is starting")
            x=pool.map(node2vec_generate_walk, g_nodes)
        elif(args.method=="deepwalk"):
            print("Deepwalk Embedding is starting")
            x=pool.map(deepwalk_generate_walk, g_nodes)
        pool.close()
        pool.join()
        walk_df=walk_df.append(x)
    
    walks_df.columns={"walk"}
    walk_df.to_pickle(args.walks_output)

    
    corpus=walks["walk"].values.tolist()
    tok_corp=[nltk.word_tokenize(sent) for sent in corpus]
  
    print("word2vec is starting")
    model=gn.models.Word2Vec(tok_corp, size=args.size, window=args.window, min_count=0,sg=1, workers=args.workers, iter=1)
    model.save(args.embedding_output)
    
if __name__=="__main__":
    args = parse_args()
    main(args)
