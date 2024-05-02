# Language-specific-Embedding

This language-specific embedding provides the implementation of embeddings on directed graphs where nodes are Wikipedia articles in different languages, and edge weights represent language-specific relatedness of those articles. 

## Embedding methods

The embedding methods used are *Deepwalk* and *Node2Vec*; Deepwalk method runs random walks on unweighted graph while Node2Vec modifies the edge weights first and then generates random walks. Then, using the generated random walks, Word2Vec algorithm learns embeddings for the nodes of the graph. 

### Input format

test2 The supported input format for embedding is an edgelist with the following columns (*See the edgelist file*):

	node1 node2 weight

And the supported input format for groundtruth dataset is as follows (*see the groundtruth_edges file*):

	node1 node2 count

## Output

The embedding results are saved as a word2vec model and generated random walks per each node of the graphs.


## Wikipedia Clickstream

Using the similarities of nodes of the graph (based on embedding results), we learn rankings for [Wikipedia clickstream](https://dumps.wikimedia.org/other/clickstream/readme.html) and evaluate results compared to the ground-truth dataset, which shows how many times a target Wikipedia article is clicked after visiting the source article. To compute similarities of nodes for groundtruth dataset, run *similarity_mapping.py* and to evaluate the results, run *evaluation.py*. 
