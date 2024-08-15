import  graph_text_encoder
import random
import networkx as nx
def self_deepwalk(node_list,edge_list,num_of_walks,max_length,is_random,start_nodes='None',):
    graph=nx.Graph()
    for node in node_list:
       graph.add_node(node)
    graph.add_edges_from(edge_list)
    all_walks=[]
    for start_node in start_nodes:
        step_walks=[]
        for i in range(num_of_walks):
            if is_random:
                random_node=random.sample(node_list,k=1)[0]
            else:
                random_node=start_node
            now_walk=[random_node]
            max_find=0
            try:
                while len(now_walk)<max_length and max_find<30 and len(list(graph.neighbors(random_node)))>0:
                    max_find+=1
                    neighbor_nodes=list(graph.neighbors(random_node))
                    choice_node=random.choice(neighbor_nodes)
                    if choice_node not in now_walk:
                        random_node=choice_node
                        now_walk.append(choice_node)
                        continue
            except:
                now_walk=[random_node]
            step_walks.append(now_walk)
        all_walks.append(step_walks)
    return all_walks

def Task_of_CycleCheck(graphs_dict,
      encoding_method,
      ):
    """The graph task to check if there is at least one cycle or not."""

    examples_dict = {}
    for ind, graph in graphs_dict.items():
      task_description = '\nQ: Is there at least one cycle in this graph? You just need to give me the final answer.\nA: '
      new_question = graph_text_encoder.encode_graph(graph['node_list'],graph['edge_list'], encoding_method,is_directed=False)
          
      sequences_in,sequences_out=graph['indegree_list'],graph['outdegree_list']
      for k in range(len(sequences_in)):
         new_question+='The indegree of node %s is %s. '%(str(k),sequences_in[k])
         new_question+='The outdegree of node %s is %s. '%(str(k),sequences_out[k])
      
      new_question+=task_description

      initial_question =graph_text_encoder.encode_graph(graph['node_list'],graph['edge_list'], encoding_method,is_directed=False)
      initial_question+=task_description

      examples_dict[ind] = {
          'new_question': new_question,
          'initial_question':initial_question,
          'answer': graph['answer'],
          'nnodes': str(len(graph['node_list'])),
          'nedges': str(len(graph['edge_list'])),
          'nodes_list':graph['node_list'],
          'edge_list':graph['edge_list'],
          
      }
    return examples_dict

def  Task_of_EulerGraph(graphs_dict,
      encoding_method,
      ):
    """The graph task to check if this graph is an euler graph on undirected graph."""

    examples_dict = {}
    for ind, graph in graphs_dict.items():
      task_description = '\nQ: Is this graph an euler graph? You just need to give me the final answer.\nA: '
      new_question = graph_text_encoder.encode_graph(graph['node_list'],graph['edge_list'], encoding_method,is_directed=False)
      new_question+='Now you need to check if this graph is an euler graph or not. There is some useful information of node degrees in this graph may help you reason by using relative algorithm. '
      
      sequences=graph['degree_list']
      for k in range(len(sequences)):
         new_question+='The degree of node %s is %s. '%(str(k),sequences[k])
      new_question+=task_description
      
      initial_question =graph_text_encoder.encode_graph(graph['node_list'],graph['edge_list'], encoding_method,is_directed=False)
      initial_question+=task_description

      examples_dict[ind] = {
          'new_question': new_question,
          'initial_question':initial_question,
          'answer': graph['answer'],
          'nnodes': str(len(graph['node_list'])),
          'nedges': str(len(graph['edge_list'])),
          'nodes_list':graph['node_list'],
          'edge_list':graph['edge_list'],
          'path_list':sequences
      }
    return examples_dict

def Task_of_Path_existence(graphs_dict,
      encoding_method,
      ):
    """The graph task to check if there is a path from a source to target on undirected graph."""
    examples_dict = {}
    for ind, graph in graphs_dict.items():
      task_description = '\nQ: Is there a path between node %s and node %s? You just need to give me the final answer.\nA: '% (
          str(graph['task_node'][0]),
          str(graph['task_node'][1]),
      )
      new_question = graph_text_encoder.encode_graph(graph['node_list'],graph['edge_list'], encoding_method,is_directed=False)

      new_question+="Now you need to check if there is a path between two nodes. There is some useful information of paths in this graph may help you reason by using relative algorithm. These paths are represented by list and each element in the list represents a node. "
      
      sequences=self_deepwalk(graph['node_list'],graph['edge_list'],num_of_walks=10,max_length=len(graph['node_list']),start_nodes=graph['task_node'],is_random=False)
      
      new_question+='These paths are start from node %s: '%graph['task_node'][0]
      for k in range(len(sequences[0])-1):
        if len(sequences[0][k])>1:
          new_question+="%s," %sequences[0][k]
      new_question+="%s. " %sequences[0][-1]

      new_question+='These paths are start from node %s: '%graph['task_node'][1]
      for k in range(len(sequences[1])-1):
        if len(sequences[0][k])>1:
          new_question+="%s," %sequences[1][k]
      new_question+="%s. " %sequences[1][-1]

      new_question+=task_description
      
      initial_question =graph_text_encoder.encode_graph(graph['node_list'],graph['edge_list'], encoding_method,is_directed=False)
      initial_question+=task_description

      examples_dict[ind] = {
          'new_question': new_question,
          'initial_question':initial_question,
          'answer': graph['answer'],
          'nnodes': str(len(graph['node_list'])),
          'nedges': str(len(graph['edge_list'])),
          'node_ids': graph['task_node'],
          'nodes_list':graph['node_list'],
          'edge_list':graph['edge_list'],
          'path_list':sequences
      }
    return examples_dict

def Task_of_Path_existence_directed(graphs_dict,encoding_method):
    """The graph task to check if there is a path from a source to target on directed graph."""
    examples_dict = {}
    for ind, graph in graphs_dict.items():
      task_description = '\nQ: Is there a path from node %s and node %s? You just need to give me the final answer.\nA: '% (
          str(graph['task_node'][0]),
          str(graph['task_node'][1]),
      )
      new_question = graph_text_encoder.encode_graph(graph['node_list'],graph['edge_list'], encoding_method,is_directed=True)

      new_question+="Now you need to check if there is a path from the node to another node. There is some useful information of paths in this graph may help you reason by using relative algorithm. These paths are represented by list and each element in the list represents a node. "
      
      sequences=self_deepwalk(graph['node_list'],graph['edge_list'],num_of_walks=10,max_length=len(graph['node_list']),start_nodes=graph['task_node'],is_random=False)
      
      new_question+='These paths are start from node %s: '%graph['task_node'][0]
      for k in range(len(sequences[0])-1):
        if len(sequences[0][k])>1:
          new_question+="%s," %sequences[0][k]
      new_question+="%s. " %sequences[0][-1]

      new_question+=task_description
      
      initial_question =graph_text_encoder.encode_graph(graph['node_list'],graph['edge_list'], encoding_method,is_directed=True)
      initial_question+=task_description

      examples_dict[ind] = {
          'new_question': new_question,
          'initial_question':initial_question,
          'answer': graph['answer'],
          'nnodes': str(len(graph['node_list'])),
          'nedges': str(len(graph['edge_list'])),
          'node_ids': graph['task_node'],
          'nodes_list':graph['node_list'],
          'edge_list':graph['edge_list'],
          'path_list':sequences
      }
    return examples_dict


def Task_of_EulerGraph_directed(graphs_dict,encoding_method):
    """The graph task to check if this graph is an euler graph on directed graph."""

    examples_dict = {}
    for ind, graph in graphs_dict.items():
      task_description = '\nQ: Is this graph an euler graph? You just need to give me the final answer.\nA: '
      new_question = graph_text_encoder.encode_graph(graph['node_list'],graph['edge_list'], encoding_method,is_directed=True)
      new_question+='Now you need to check if this graph is an euler graph or not. There is some useful information of node degrees in this graph may help you reason by using relative algorithm. '
      sequences_in,sequences_out=graph['indegree_list'],graph['outdegree_list']
      for k in range(len(sequences_in)):
         new_question+='The indegree of node %s is %s. '%(str(k),sequences_in[k])
         new_question+='The outdegree of node %s is %s. '%(str(k),sequences_out[k])
      new_question+=task_description
      
      initial_question =graph_text_encoder.encode_graph(graph['node_list'],graph['edge_list'], encoding_method,is_directed=True)
      initial_question+=task_description

      examples_dict[ind] = {
          'new_question': new_question,
          'initial_question':initial_question,
          'answer': graph['answer'],
          'nnodes': str(len(graph['node_list'])),
          'nedges': str(len(graph['edge_list'])),
          'nodes_list':graph['node_list'],
          'edge_list':graph['edge_list'],
          
      }
    return examples_dict


def Task_of_CycleCheck_directed(graphs_dict,encoding_method):
    """The graph task to check if there is at least one cycle or not."""

    examples_dict = {}
    for ind, graph in graphs_dict.items():
      task_description = '\nQ: Is there at least one cycle in this graph? You just need to give me the final answer.\nA: '
      new_question = graph_text_encoder.encode_graph(graph['node_list'],graph['edge_list'], encoding_method,is_directed=True)
        
      new_question+="Now you need to check if there is at least one cycle in graph or not. There is some useful information of node degrees in this graph may help you reason by using relative algorithm. "
      sequences_in,sequences_out=graph['indegree_list'],graph['outdegree_list']
      for k in range(len(sequences_in)):
         new_question+='The indegree of node %s is %s. '%(str(k),sequences_in[k])
         new_question+='The outdegree of node %s is %s. '%(str(k),sequences_out[k])
      new_question+=task_description
      
      initial_question =graph_text_encoder.encode_graph(graph['node_list'],graph['edge_list'], encoding_method,is_directed=True)
      initial_question+=task_description

      examples_dict[ind] = {
          'new_question': new_question,
          'initial_question':initial_question,
          'answer': graph['answer'],
          'nnodes': str(len(graph['node_list'])),
          'nedges': str(len(graph['edge_list'])),
          'nodes_list':graph['node_list'],
          'edge_list':graph['edge_list'],
      }
    return examples_dict



TASK_CLASS = {
    'cycle_check':  Task_of_CycleCheck,
    'Path_existence': Task_of_Path_existence,
    'euler_graph': Task_of_EulerGraph,
    'Path_existence_directed':Task_of_Path_existence_directed,
    'cycle_check_directed':Task_of_CycleCheck_directed,
    'euler_graph_directed':Task_of_EulerGraph_directed
    
    }
