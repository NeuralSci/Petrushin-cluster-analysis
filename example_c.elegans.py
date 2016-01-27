import petrushin_cluster_analysis as pca
import networkx as nx

table = {}
for line in open("c.elegans_connectome.txt", "r"):
    myline = line.split()
    table[myline[0]] = [myline[i] for i in xrange(1,len(myline))]
    
# Multigraph inizialization (allows multiple connections between two nodes)
G = nx.MultiDiGraph() 
for key in table:   
    G.add_node(key)
    for n in table.get(key):
        G.add_edge(key, n)
G = G.reverse()
G.remove_edges_from(G.selfloop_edges()) # remove selfloops (RIBR, RIBL and VA8)

cluster, info = pca.find_clusters(G, "power", "23", True) 
