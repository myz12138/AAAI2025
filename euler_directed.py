import random
from collections import defaultdict
import networkx as nx

def balance_graph(G):
    graph={node:list(G.neighbors(node)) for node in G.nodes()}
    in_degree = defaultdict(int)
    out_degree = defaultdict(int)

    for u in graph:
        out_degree[u] = len(graph[u])
        for v in graph[u]:
            in_degree[v] += 1

    extra_out = [node for node in graph if in_degree[node] > out_degree[node]]
    extra_in = [node for node in graph if out_degree[node] > in_degree[node]]

    new_edges = []
    i,j= 0,0
    while  j < len(extra_out):
        
        u, v = extra_out[j], extra_in[i]
        if (u,v) not in new_edges:
            new_edges.append((u, v))
            out_degree[u] += 1
            in_degree[v] += 1
        i+=1
        if i==len(extra_in) or out_degree[u] == in_degree[u]:
            extra_out.remove(u)
            j = 0
            i = 0
    G.add_edges_from(new_edges)
    return G

def generate_euler_graph(n):
    edge_probability=0.3
    G=nx.DiGraph()
    G.add_nodes_from([i for i in range(n)])
    
    for i in range( n):
        G.add_edge(i, (i+1)%n)
    for i in range(n):
        for j in range(n):
            if i != j and random.random() < edge_probability and (i,j) not in G.edges() and (j,i) not in G.edges():
                G.add_edge(i, j)
                G.add_edge(j,i)
    
    return G

def generate_non_euler_graph(n):
    graph = {i: set() for i in range(n)}
    edges = []
    
    for i in range(n):
        out_degree = random.randint(0, n-1)
        for _ in range(out_degree):
            j = random.randint(0, n-1)
            if j != i and j not in graph[i]:
                graph[i].add(j)
                edges.append((i, j))

    for i in range(1, n):
        if i not in graph[0]:
            graph[0].add(i)
            edges.append((0, i))
    
    if len(graph[0]) == sum(1 for i in range(n) if 0 in graph[i]):
        j = random.randint(1, n-1)
        graph[0].add(j)
        edges.append((0, j))
    G=nx.DiGraph()
    G.add_nodes_from([i for i in range(n)])
    G.add_edges_from(edges)
    
    return G

if __name__=="__main__":

    n = 5  
    euler= generate_euler_graph(n)
    try:
        print(nx.is_eulerian(euler))
        print('Yes') 
    except nx.NetworkXError:
        print('No') 
    non_euler=generate_non_euler_graph(n)
    try:
        print(nx.is_eulerian(non_euler))
        print('Yes') 
    except nx.NetworkXError:
        print('No') 
