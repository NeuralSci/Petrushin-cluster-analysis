INTRODUCTION
============

This package implements the algorithm presented in paper “Optimization of an electro-optical representation of the C. elegans connectome through neural network cluster analysis”.  The algorithm is implemented in `python 2.7`. 

The algorithm divides the network connectome into three clusters. Two of these clusters are not interconnected. Other two clusters are independent which means that there are no edges between them unless a node has no inter-cluster successors. 

Algorithm is capable to handle directed unweighted graphs. The algorithm runs at time O(n2). The core function is `find_clusters` which finds the biggest independent cluster or the best clustering solution for the power optimization. 

INSTALLATION
============

Copy the `petrushin_cluster_analysis.py` to the same directory of your code.

USAGE
=====

In order to use function you will need the python to be installed on your machine. 
Import the packages:
```python
import petrushin-cluster-analysis as pca
import networkx as nx
```
For testing purposes a random directed graph is created:
```python
G = nx.gnm_random_graph(50, 400, None, True)
```
To find clusters use:
```python
cluster, info = pca.find_clusters(G, criterion = "size", parameter = "max", exclude_inter = False)
```
`cluster` contains the list of nodes of the found clusters. `info` contains information about found clusters (original nodes, size, power saving). 

REFERENCES
==========

Please cite the references appropriately in case it is used.

1.	Alexey Petrushin, Lorenzo Ferrara and Axel Blau. " Optimization of an electro-optical representation of the C. elegans connectome    through neural network cluster analysis" Neural Networks (IJCNN), 2016 International Joint Conference on. IEEE, 2016. 


