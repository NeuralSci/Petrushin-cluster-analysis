"""
This module implements petrushin cluster algorithm

The algorithm divides the network into three clusters: R, B and G.
Two of these clusters (R, B) are not interconnected, whereas the third cluster (G)
 is strongly connected to both R and B.

Clustering can be done by two criteria: 
1) clustering for optimal power 

P=(1-A_(after clust)/A_(before clust) )*100%
A_(before clust) is equal to the square of the number of neurons in the network. A_(after clust) is calculated as:
A_(after clust)=R(R+G)+B(B+G)+G*G
where R, B and G are the numbers of elements in the R, B and G clusters, respectively 

2) clustering for maximum cluster size. find the solution with the maximum number of nodes for in R and B clusters 

Basic example (solution for optimal power)
    --------
    >>> import petrushin_cluster_analysis as pca
    >>> import networkx as nx  
    >>> G = nx.gnm_random_graph(50, 490, None, True)
    >>> cluster, info = pca.find_clusters(G, "power", "max", False) 
"""
#    Copyright (C) 2016 by
#    Alexey Petrushin <a.petrushin@mail.ru>
#    All rights reserved.
#    GNU GENERAL PUBLIC LICENSE V3.

import networkx as nx
import itertools

def excluding_inter_connections(G, info):
    """
    Eliminates neurons that have output connections from cluster R to cluster B and vice versa. 
    Returns the new clusters R and B. 
    
    Parameters    
    ----------
    G : graph
    info : two-dimensional list 
       info[0] - list of cluster R nodes  , info[1] - list of cluster B nodes  
    
    Returns
    -------
    info : two-dimensional list 
       A list of nodes for new clusters R and B

    """
    temp = [[], []]
    for m in xrange(len(info)):
        for key1 in info[m]:
            in_con, out_con = 0, 0
            for x in xrange(len(info)):
                for key2 in info[x]: 
                    if x == m and in_con == 0:
                        if G.has_edge(key1, key2):
                            in_con = 1
                    if x != m and out_con == 0:
                        if G.has_edge(key1, key2):
                            out_con = 1
                    if in_con == 1 and out_con == 1:
                        break
            if in_con == 0 and out_con == 1:
                temp[m].append(key1)
            
    for j in xrange(len(info)):
        temp[j] = list(set(temp[j]))
        info[j] = list(set(info[j]) - set(temp[j]))
         
    return info   

def unique_sucsessors(G, info):
    """
    Finds unique sucsessors (nodes that have output connections to only 1 cluster) 
    for the nodes in the clusters R and B and includes them in the clusters   
    Returns the new clusters R and B. 
    
    Parameters    
    ----------
    G : graph
    info : two-dimentional list 
       info[0] - list of cluster R nodes  , info[1] - list of cluster B nodes
    
    Returns
    -------
    info : two-dimentional list 
       A list of nodes for new clusters R and B
    """   
       
    temp1 = []
    for n in xrange(len(info)):
        temp = []
        for key in info[n]:
            temp.append(G.successors(key))
        temp = list(itertools.chain.from_iterable(temp))   
        temp1.append(temp)

    # find unique sets of postsinaptic neurons for each cluster
    info[0] += list(set(temp1[0]) - set(temp1[1])) 
    info[1] += list(set(temp1[1]) - set(temp1[0]))    

    temp = [[], []]
    for m in xrange(len(info)):
        for key1 in info[m]:
            in_con, out_con = 0, 0
            for x in xrange(len(info)):
                for key2 in info[x]:  
                    if x == m and in_con == 0:
                        if G.has_edge(key1, key2):
                            in_con = 1
                    if x != m and out_con == 0:
                        if G.has_edge(key1, key2):
                            out_con = 1
                    if in_con == 1 and out_con == 1:
                        break
            if in_con == 1 and out_con == 1:
                temp[m].append(key1)
            
    for j in xrange(len(info)):
        temp[j] = list(set(temp[j]))
        info[j] = list(set(info[j]) - set(temp[j]))
              
    return info   

def create_table(G):
    """
    Returns a list of node pairs (original nodes for R and B clusters)
    
    Parameters    
    ----------
    G : graph
    
    Returns
    -------
    mylist : two-dimensional list 
       A list of original node pairs
    """       
    node_list = G.nodes()
    mylist, b = [], 0
    for key in G.nodes():
        b += 1
        for x in xrange(b, len(node_list)):
            temp = []
            if node_list[x] not in G.successors(key):
                if node_list[x] not in G.predecessors(key):
                    temp = [key, node_list[x]]
                    mylist.append(temp)
    return mylist


def find_single_solution(G, info):
    """
    Returns a list of nodes in cluster R and in cluster B 
    
    Parameters    
    ----------
    G : graph
    info: list containing a pair of original nodes
    
    Returns
    -------
    info : two-dimensional list 
       info[0] - list of cluster R nodes  , info[1] - list of cluster B nodes
    """         
    
    length1, length2, check, n = 0, 0, 1, 0
    while check > 0:
        n = n + 1
        info = unique_sucsessors(G, info)
        if (length1 < len(info[0])) or (length2 < len(info[1])):
                length1 = len(info[0])
                length2 = len(info[1])
        else:
            check = check - 1
        if n > 15:
            check = check - 1 
    return info

def find_clusters(G, criterion = "power", parameter = "max", exclude_inter = False):
    """
    Returns a list of nodes in cluster R and in cluster B and information about these nodes. 
    Returned cluster can either have the biggest sum of nodes or result in best power savings      
    
    Parameters    
    ----------
    G : graph
    criterion: "power" - find solution with optimized for power (distribution with the best optical power saving)
               "size"  - find solution optimized for size (the biggest sum of nodes in R and B clusters)
    parameter: "max"   - find the best solution 
               "N" (when criterion = "power") - find all solutions with power saving > N 
                               (N - a number between 0 and 50, percentage of power saving)
               "N" (when criterion = "size") - find all solution with R + B > N (N - an integer number)
    exclude_inter: False - Do not eliminates neurons that have output connections from cluster R to cluster B and vice versa 
                   True - "no" - Eliminates neurons that have output connections from cluster R to cluster B and vice versa               
    
    Returns
    -------
    cluster : two-dimensional list 
       cluster[0] - list of cluster R nodes, cluster[1] - list of cluster B nodes
    info_cluster: information about clusters (original nodes, cluster size, power saving) 
    """         
   
    origins = create_table(G)
    nodes = G.number_of_nodes()
    p_after, p_eff, p_eff_max, max_len1, max_len2 = 0.0, 0.0, 0.0, 0, 0
    p_before, info_cluster, cluster  = nodes * nodes, [], [[],[]]
    for x in xrange(len(origins)):
        if x % 40 == 0:
            print round(100* x / float(len(origins)), 2), "% done"
        key1, key2 = origins[x][0], origins[x][1]
        temp = find_single_solution(G, [[key1], [key2]])
        if exclude_inter == True:
            temp = excluding_inter_connections(G, temp)
        length1 = float(len(temp[0]))
        length2 = float(len(temp[1]))           
        a = nodes - length1 - length2
        p_after = length1 * (length1 + a) + length2 * (length2 + a) + nodes * a
        p_eff = 100 * (1 - (p_after/p_before))        
        
        if criterion == "power":
            if parameter == "max":
                if  p_eff > p_eff_max and length1 != 0 and length2 != 0:
                    max_len1, max_len2, p_eff_max = length1, length2, p_eff
                    max_key1, max_key2, = key1, key2
                    cluster = temp
                    info_cluster = ["Node1:", max_key1, "Node2:", max_key2, "R size:", int(max_len1), "B size:", int(max_len2), "P saving (max):", round(p_eff_max, 2)] 
            else:
                if p_eff > int(parameter) and length1 != 0 and length2 != 0:
                    info_cluster.append(["Node1:", key1, "Node2:", key2, "R size:", int(length1), "B size:", int(length2), "P saving:", round(p_eff, 2)])
                    if p_eff_max < p_eff:
                        p_eff_max = p_eff
                        cluster = temp
        if criterion == "size":
            if parameter == "max":
                if  max_len1 + max_len2 < length1 + length2 and length1 != 0 and length2 != 0:
                    max_len1, max_len2, p_eff_max = length1, length2, p_eff
                    max_key1, max_key2, = key1, key2
                    cluster = temp
                    info_cluster = ["Node1:", max_key1, "Node2:", max_key2, "R size:", int(max_len1), "B size:", int(max_len2), "Size R+B(max):", max_len1 + max_len2, "P saving:", round(p_eff_max, 2)] 
            else:
                if length1 + length2 > int(parameter) and length1 != 0 and length2 != 0:
                    info_cluster.append(["Node1:", key1, "Node2:", key2, "R size:", int(length1), "B size:", int(length2), "Size R+B:", length1 + length2, "P saving:", round(p_eff, 2)])
                    if p_eff_max < p_eff:
                        p_eff_max = p_eff
                        cluster = temp             

               
    return cluster, info_cluster
