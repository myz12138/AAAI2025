import networkx as nx
import random

def create_eulerian_graph(num_nodes):
    while True:
        G = nx.Graph()
        G.add_nodes_from(range(num_nodes))

        for i in range(1, num_nodes):
            G.add_edge(i-1, i)

        for _ in range(random.randint(0, num_nodes)):
            u = random.randint(0, num_nodes-1)
            v = random.randint(0, num_nodes-1)
            if u != v and not G.has_edge(u, v):
                G.add_edge(u, v)
        odd_degree_nodes = [n for n in G.nodes() if G.degree(n) % 2 != 0]
        while odd_degree_nodes:
            u = odd_degree_nodes.pop()
            v = odd_degree_nodes.pop()
            G.add_edge(u, v)
        
        if nx.is_connected(G) and all(G.degree(n) % 2 == 0 for n in G.nodes()):
            return G

def create_non_eulerian_graph(num_nodes):
    while True:
        G = nx.Graph()
        G.add_nodes_from(range(num_nodes))

        for i in range(1, num_nodes):
            G.add_edge(i-1, i)

        for _ in range(random.randint(0, num_nodes)):
            u = random.randint(0, num_nodes-1)
            v = random.randint(0, num_nodes-1)
            if u != v and not G.has_edge(u, v):
                G.add_edge(u, v)
        
        if all(G.degree(n) % 2 == 0 for n in G.nodes()):
            node = random.choice(list(G.nodes()))
            neighbor = random.choice(list(G.neighbors(node)))
            G.remove_edge(node, neighbor)
        
        if nx.is_connected(G) and any(G.degree(n) % 2 != 0 for n in G.nodes()):
            return G


if __name__=="__main__":

    num_nodes = 50 
    eulerian_graph = create_eulerian_graph(num_nodes)
    non_eulerian_graph = create_non_eulerian_graph(num_nodes)
