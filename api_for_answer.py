import openai
from os import getenv
import json
import os
from openai import OpenAI
import random
import time
MAX_RETRIES = 5 
RETRY_DELAY = 10  


def read_json(jsonfile_path):
    
    f = open(jsonfile_path, 'r')
    content = f.read()
    a = json.loads(content)
    
    f.close()
    return a
def retry_on_payment_required(func, args, kwargs):
        retries = 0
        flag = True
        while retries < MAX_RETRIES:
            try:
                
                return func(args[0], kwargs) , flag
            except Exception as e:
                raise e
def create_completion(model, messages):
    return client.chat.completions.create(
            model=model,
        messages=messages
    )

if __name__=="__main__":
    task_list=['path_existence','euler_graph','cycle_check']
    type_list=['hard','medium','easy']
    for task in task_list:
        for data_type in type_list:
            model_name=""
            data_file='undirected_data'
            answer_dic={}

            jsonfile_path='./'+data_file+'/'+task+'/'+data_type+'/'+task+'_examples.json'
            json_file=read_json(jsonfile_path)


            write_path='./'+data_file+'/'+task+'/'+data_type+'/answer_of_'+task+'_'+model_name+'.json'
            write_file=read_json(write_path)
            client=OpenAI(
                api_key='',
                base_url=''
            )
        
            print('start %s for %s for %s on %s graph'%(model_name,data_file,task,data_type))
           
            for key,value in json_file.items():
                
                
                model=model_name,
                messages_initial=[
                    {
                        'role':"system",
                        "content":"You are a graph analyst and you must need to give me the final answer. Do not give any reasoning or logic for your answer."
                    },
                {
                "role": "user",
                "content": value['initial_question'],
                }]
                messages_new=[
                        {
                        'role':"system",
                        "content":"You are a graph analyst and you must need to give me the finial answer. Do not give any reasoning or logic for your answer."
                    },
                {
                "role": "user",
                "content": value['new_question'],
                }]

                completion_initial, flag_initial = retry_on_payment_required(create_completion, model, messages_initial)
                answer_dic[key]={"real_answer":value['answer'],"api_answer_initial": completion_initial.choices[0].message.content,"api_answer_new":""}
                completion_new, flag_new = retry_on_payment_required(create_completion, model, messages_new)
                answer_dic[key]["api_answer_new"]=completion_new.choices[0].message.content   
                print(key,":",answer_dic[key])
                answer_dic[key]['initial_judge'],answer_dic[key]['new_judge']='',''
                write_file.update({key:answer_dic[key]})
                with open('./'+data_file+'/'+task+'/'+data_type+'/answer_of_'+task+'_'+model_name+'.json', 'w',encoding='utf-8') as f:
                    b = json.dump(write_file,f,indent=1)
                
        
        

