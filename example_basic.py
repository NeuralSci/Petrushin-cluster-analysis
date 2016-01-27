import petrushin_cluster_analysis as pca
import networkx as nx

G = nx.gnm_random_graph(50, 400, None, True)
cluster, info = pca.find_clusters(G, criterion = "size", "max", False) 
