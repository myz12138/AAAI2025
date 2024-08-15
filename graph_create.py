'''
    Target:  create graphs for different graph task
    Input:   (name_of_task,number_of_graphs,is_directed,graph_scale)
    Output:  json_file(node_list,edge_list,is_directed,graph_scale,task_node)
'''
import networkx as nx
import random
import json
import numpy as np
import os
import euler_undirected
import euler_directed
_NUMBER_OF_NODES_RANGE = {
    "easy":  (5, 15),
    "medium":  (16, 25),
    "hard":  (26,35),
}

 #func of add_edge based probability
def rand_edge(G,vi, vj, p): 
    probability = random.random()
    if probability > p:
        G.add_edge(vi, vj) 
        return 
    else:
        not_existence_edges=(vi,vj)
        return not_existence_edges

def Graphs_for_CycleCheck(number_of_graphs,graph_scale,is_directed):
    graphs={}
    #graph generator
    cycle_p={
        #undirected
        "easy":  0.83,
        "medium": 0.93,
        "hard":  0.96
    }
    cycle_p2={
        #undirected
        "easy":  0.83,
        "medium": 0.93,
        "hard":  0.96,

    }
    for i in range(number_of_graphs):

        G = nx.Graph() 
        num_nodes =random.randint( _NUMBER_OF_NODES_RANGE[graph_scale][0],_NUMBER_OF_NODES_RANGE[graph_scale][1])
        G.add_nodes_from([node for node in range(num_nodes)]) 
        for node1 in range(num_nodes):
            for node2 in range(node1):
                probability = random.random()
                if probability >cycle_p[graph_scale]:
                    G.add_edge(node1, node2) 
                if probability >cycle_p2[graph_scale]:
                    G.add_edge(node2, node1) 
        graphs[i]={
            'node_list':list(G.nodes()),
            'edge_list':list(G.edges()),
            'direct_bool':is_directed,
            'scale':graph_scale,
            'task':'cycle_check'
        }
        
        if is_directed:
            graphs[i]['indegree_list']=[G.in_degree(i) for i in list(G.nodes())]
            graphs[i]['outdegree_list']=[G.out_degree(i) for i in list(G.nodes())]
        else:
            graphs[i]['degree_list']=[G.degree(i) for i in list(G.nodes())]
        
        try:
            path=[u for u,v in nx.find_cycle(G)]
            graphs[i]['answer']='Yes'
        except nx.NetworkXNoCycle:
            graphs[i]['answer']='No'

    return graphs
    

def Graphs_for_Path_existence(number_of_graphs,graph_scale,is_directed):
    graphs={}
    #graph generator
    Reachability_p={
        #undirected
        "easy":  0.81,
        "medium": 0.91,
        "hard":  0.93
    }
    for i in range(number_of_graphs):
        G = nx.Graph() 
        num_nodes =random.randint( _NUMBER_OF_NODES_RANGE[graph_scale][0],_NUMBER_OF_NODES_RANGE[graph_scale][1])
        G.add_nodes_from([node for node in range(num_nodes)]) 
        for node1 in range(num_nodes):
            for node2 in range(node1):
                probability = random.random()
                if probability > Reachability_p[graph_scale]:
                    G.add_edge(node1, node2) 
                if probability > Reachability_p[graph_scale]:
                    G.add_edge(node2, node1) 
            
           
        graphs[i]={
            'node_list':list(G.nodes()),
            'edge_list':list(G.edges()),
            'direct_bool':is_directed,
            'scale':graph_scale,
            'task':'Path_existence'
        }
    #task_specialized node generator
        source, target = random.sample(list(G.nodes()), k=2)
        graphs[i]['task_node']=[source, target]
        if nx.has_path(G, source, target):
            graphs[i]['answer'] = 'Yes'
        else:
            graphs[i]['answer']  = 'No'
    return graphs
 


def Graphs_for_EulerGrpah(number_of_graphs,graph_scale,is_directed):
    graphs={}
    #graph generator
    for i in range(number_of_graphs):
        num_nodes =random.randint( _NUMBER_OF_NODES_RANGE[graph_scale][0],_NUMBER_OF_NODES_RANGE[graph_scale][1])
        if random.random()<0.5:
            G = euler_undirected.create_eulerian_graph(num_nodes)
        else:
            G=euler_undirected.create_non_eulerian_graph(num_nodes)
        graphs[i]={
            'node_list':list(G.nodes()),
            'edge_list':list(G.edges()),
            'direct_bool':is_directed,
            'scale':graph_scale,
            'task':'euler_graph'
        }
        graphs[i]['degree_list']=[G.degree(i) for i in list(G.nodes())]
       
        try:
            path = [u for u, v in nx.eulerian_circuit(G,keys=False)]
            graphs[i]['answer'] ='Yes' 
        except nx.NetworkXError:
            graphs[i]['answer'] = 'No'
    
        
    return graphs

def DirectedGraphs_for_Path_existence(number_of_graphs,graph_scale,is_directed):
    graphs={}
    #graph generator
    Reachability_p={
        "easy":  0.81,
        "medium": 0.91,
        "hard":  0.93
    }
    for i in range(number_of_graphs):
        G = nx.DiGraph()
        num_nodes =random.randint( _NUMBER_OF_NODES_RANGE[graph_scale][0],_NUMBER_OF_NODES_RANGE[graph_scale][1])
        G.add_nodes_from([node for node in range(num_nodes)]) 
        not_existence_edges=[]
        for node1 in range(num_nodes):
            for node2 in range(node1):
                probability = random.random()
                if probability > Reachability_p[graph_scale]:
                    G.add_edge(node1, node2) 
                else:
                    not_existence_edges.append((node1,node2))  
        graphs[i]={
            'node_list':list(G.nodes()),
            'edge_list':list(G.edges()),
            'direct_bool':is_directed,
            'scale':graph_scale,
            'task':'Path_existence'
        }

        source, target = random.sample(list(G.nodes()), k=2)
        graphs[i]['task_node']=[source, target]
        if nx.has_path(G, source, target): 
            graphs[i]['answer'] = 'Yes'
        else:
            graphs[i]['answer']  = 'No'
        
    return graphs
    

def DirectedGraphs_for_cycle_check(number_of_graphs,graph_scale,is_directed):
    graphs={}
    #graph generator
    cycle_p={

        "small":  0.89,
        "medium": 0.95,
        "large":  0.97,
    }
    
    for i in range(number_of_graphs):
        G = nx.DiGraph()
        num_nodes =random.randint( _NUMBER_OF_NODES_RANGE[graph_scale][0],_NUMBER_OF_NODES_RANGE[graph_scale][1])
        G.add_nodes_from([node for node in range(num_nodes)]) 
        for node1 in range(num_nodes):
            for node2 in range(num_nodes):
                probability = random.random()
                if probability >cycle_p[graph_scale] and node1!=node2:
                    G.add_edge(node1, node2) 
        graphs[i]={
            'node_list':list(G.nodes()),
            'edge_list':list(G.edges()),
            'direct_bool':is_directed,
            'scale':graph_scale,
            'task':'cycle_check'
        }
        
      
        graphs[i]['indegree_list']=[G.in_degree(i) for i in list(G.nodes())]
        graphs[i]['outdegree_list']=[G.out_degree(i) for i in list(G.nodes())]
        try:
            path=[u for u,v in nx.find_cycle(G)]
            graphs[i]['answer']='Yes'
        except nx.NetworkXNoCycle:
            graphs[i]['answer']='No'

    return graphs


def DirectedGraphs_for_euler_graph(number_of_graphs,graph_scale,is_directed):
    graphs={}
    
    #graph generator
    for i in range(number_of_graphs):
        num_nodes =random.randint( _NUMBER_OF_NODES_RANGE[graph_scale][0],_NUMBER_OF_NODES_RANGE[graph_scale][1])
        
        if random.random()<0.5:
            G = euler_directed.generate_euler_graph(num_nodes)
        else:
            G=euler_directed.generate_non_euler_graph(num_nodes)
           
        graphs[i]={
            'node_list':list(G.nodes()),
            'edge_list':list(G.edges()),
            'direct_bool':is_directed,
            'scale':graph_scale,
            'task':'euler_graph'
        }
       
        graphs[i]['indegree_list']=[G.in_degree(i) for i in list(G.nodes())]
        graphs[i]['outdegree_list']=[G.out_degree(i) for i in list(G.nodes())]
        try:
            path = [u for u, v in nx.eulerian_circuit(G,keys=False)]
            graphs[i]['answer'] ='Yes' 
        except nx.NetworkXError:
            graphs[i]['answer'] = 'No'

        
    return graphs


GRAPH_CLASS = {
    'cycle_check':  Graphs_for_CycleCheck,
    'reachability': Graphs_for_Path_existence,
    'euler_graph':Graphs_for_EulerGrpah,
    'reachability_directed':DirectedGraphs_for_Path_existence,
    'cycle_check_directed':DirectedGraphs_for_cycle_check,
    'euler_graph_directed':DirectedGraphs_for_euler_graph
    
    }

def default_dump(obj):
    """Convert numpy classes to JSON serializable objects."""
    if isinstance(obj, (np.integer, np.floating, np.bool_)):
        return obj.item()
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj

