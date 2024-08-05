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
    "small":  (5, 15),
    "medium":  (16, 25),
    "large":  (26,35),
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
        # "small":  0.83,
        # "medium": 0.93,
        # "large":  0.96,

        #directed
        "small":  0.6,
        "medium": 0.01,
        "large":  0.01,
    }
    cycle_p2={
        #undirected
        # "small":  0.83,
        # "medium": 0.93,
        # "large":  0.96,

        #directed
        "small":  0.98,
        "medium": 1,
        "large":  1,
    }
    for i in range(number_of_graphs):
        if not is_directed:
            G = nx.Graph() 
        else:
            G = nx.DiGraph()
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
        
        #task_specialized node generator
        try:
            path=[u for u,v in nx.find_cycle(G)]
            graphs[i]['answer']='Yes'
        except nx.NetworkXNoCycle:
            graphs[i]['answer']='No'

    return graphs
    

def Graphs_for_Reachability(number_of_graphs,graph_scale,is_directed):
    graphs={}
    #graph generator
    Reachability_p={
        #undirected
        # "small":  0.82,
        # "medium": 0.91,
        # "large":  0.94

        #directed
        "small":  0.82,
        "medium": 0.91,
        "large":  0.94
    }
    for i in range(number_of_graphs):
        if not is_directed:
            G = nx.Graph() 
        else:
            G = nx.DiGraph()
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
            'task':'reachability'
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
            G = euler_directed.create_directed_eulerian_graph(num_nodes)
        else:
            G=euler_directed.create_non_eulerian_graph(num_nodes)
        
        graphs[i]={
            'node_list':list(G.nodes()),
            'edge_list':list(G.edges()),
            'direct_bool':is_directed,
            'scale':graph_scale,
            'task':'euler_graph'
        }
        if is_directed:
            graphs[i]['indegree_list']=[G.in_degree(i) for i in list(G.nodes())]
            graphs[i]['outdegree_list']=[G.out_degree(i) for i in list(G.nodes())]
        else:
            graphs[i]['degree_list']=[G.degree(i) for i in list(G.nodes())]
    #task_specialized node generator
       
        try:
            path = [u for u, v in nx.eulerian_circuit(G,keys=False)]
            graphs[i]['answer'] ='Yes' 
        except nx.NetworkXError:
            graphs[i]['answer'] = 'No'
            #'There is no euler path from node %s.' % str(source_node)
        
    return graphs


def DirectedGraph_for_cycle_check(number_of_graphs,graph_scale,is_directed):
    graphs={}
    #graph generator
    cycle_p={

        "small":  0.89,
        "medium": 0.95,
        "large":  0.97,
    }
    
    for i in range(number_of_graphs):
        if not is_directed:
            G = nx.Graph() 
        else:
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
        
        if is_directed:
            graphs[i]['indegree_list']=[G.in_degree(i) for i in list(G.nodes())]
            graphs[i]['outdegree_list']=[G.out_degree(i) for i in list(G.nodes())]
        else:
            graphs[i]['degree_list']=[G.degree(i) for i in list(G.nodes())]
        
        #task_specialized node generator
        try:
            path=[u for u,v in nx.find_cycle(G)]
            graphs[i]['answer']='Yes'
        except nx.NetworkXNoCycle:
            graphs[i]['answer']='No'

    return graphs


def DirectedGraph_for_euler_graph(number_of_graphs,graph_scale,is_directed):
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
        if is_directed:
            graphs[i]['indegree_list']=[G.in_degree(i) for i in list(G.nodes())]
            graphs[i]['outdegree_list']=[G.out_degree(i) for i in list(G.nodes())]
        else:
            graphs[i]['degree_list']=[G.degree(i) for i in list(G.nodes())]
    #task_specialized node generator
       
        try:
            path = [u for u, v in nx.eulerian_circuit(G,keys=False)]
            
            graphs[i]['answer'] ='Yes' 
        except nx.NetworkXError:
            graphs[i]['answer'] = 'No'
            
    return graphs






GRAPH_CLASS = {
    'cycle_check':  Graphs_for_CycleCheck,
    'reachability': Graphs_for_Reachability,
    'euler_graph':Graphs_for_EulerGrpah,
    'reachability_directed':Graphs_for_Reachability,
    'cycle_check_directed':DirectedGraph_for_cycle_check,
    'euler_graph_directed':DirectedGraph_for_euler_graph
    
    }

def default_dump(obj):
    """Convert numpy classes to JSON serializable objects."""
    if isinstance(obj, (np.integer, np.floating, np.bool_)):
        return obj.item()
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj

if __name__=='__main__':
    graphs=Graphs_for_CycleCheck(number_of_graphs=1000,graph_scale='medium',is_directed=False)

    k=0
    for key,value in graphs.items():
        print(value['answer'])
        if value['answer']=='Yes':
            k+=1
    print(k/len(graphs))

    task_type='cycle_check'
    scale='medium'
    dirs = './new_code/'+task_type+'/'+scale
    if not os.path.exists(dirs):
        os.makedirs(dirs)

    with open('./new_code/'+task_type+'/'+scale+'/'+task_type+'_datas.json', 'w',encoding='utf-8') as f:
        b = json.dump(graphs,f,default=default_dump,)