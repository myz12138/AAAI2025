import openai
from os import getenv
import json
import os
from openai import OpenAI
import time
MAX_RETRIES = 5  
RETRY_DELAY = 10  


def read_json(jsonfile_path):
    
    f = open(jsonfile_path, 'r')
    content = f.read()
    a = json.loads(content)
    
    f.close()
    return a
task='reachability'
data_type='medium'
model_name="claude-3-sonnet-20240229"
data_file='undirected_data'
jsonfile_path='./'+data_file+'/'+task+'/'+data_type+'/countgraph_of_'+task+'_'+model_name+'.json'
json_file=read_json(jsonfile_path)
initial,new=0,0
for key,value in json_file.items():
    print(value['initial_judge'])
    initial+=int(value['initial_judge'])
    new+=int(value['new_judge'])
print(initial/len(json_file),new/len(json_file))