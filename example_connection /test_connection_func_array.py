import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI
import json
import re
from colorama import Fore, Back, Style #Colors

#Setup creds 
load_dotenv()
llm_0_url="https://openrouter.ai/api/v1"
llm_0_key=os.getenv("OPENROUTER_API_KEY")
llm_0_model="meta-llama/llama-3.2-3b-instruct:free"

# llm_<num>_<obj> format for additonal models and API endpoints if desired 
#llm_0_url="https://openrouter.ai/api/v1"
#llm_0_key=os.getenv("OPENROUTER_API_KEY")
#llm_0_model="deepseek-ai/DeepSeek-R1"

# Set vars 
def cli_args():
    global debug_mode
    global cli_query
    global n_q
    global n_refine
    parser = argparse.ArgumentParser(description="Script with debug flag")
    parser.add_argument("-q",#required=True,
                        help="Question to research")
    parser.add_argument("-n_q",type=int,default=3,help="N of questions to answer (first refine)")
    parser.add_argument("-n_refine",type=int,default=3,help="N of refinement iterations")
    parser.add_argument("-debug",action="store_true",help="Debug Mode",)
    args = parser.parse_args()

    cli_query = args.q
    n_q = args.n_q
    n_refine = args.n_refine
    debug_mode = args.debug
    return cli_query, n_q, n_refine

#Pretty
def print_red(x):print(Fore.RED+x+Style.RESET_ALL)
def print_cyan(x):print(Fore.CYAN+x+Style.RESET_ALL)

def debug(llm_0_url,llm_0_key,llm_0_model,query):
    print(
    "llm_0_url: ",llm_0_url,
    "llm_0_key: ",llm_0_key,
    "llm_0_model: ",llm_0_model,
    "Query: ",query
    )

def llm_0(llm_0_url,llm_0_key,llm_0_model,query):
    client = OpenAI(
        base_url=llm_0_url,
        api_key=llm_0_key)

    messages = [{
                "role": "developer",
                "content": "You are a helpful research assistant. Always respond in the following JSON format: [{\"response\": {\"id\": 1,\"question\": \"Some type of question\"}}, {\"response\": {\"id\": 2,\"question\": \"Some type of question\"}}]. Do not include any extra text, explanations, or variations in formatting."
                },
                {
                "role": "user",
                "content": query
                }]

    completion = client.chat.completions.create(
        model=llm_0_model, 
        messages=messages, 
        max_tokens=500)
    
    json_results=completion.choices[0].message.content
    return json_results

def thought_loop():
    test=test
    return

def refine_question():
    LLM_QUERY="I will ask a question. Think deeply about 3 additional questions that could be asked that would help understand the problem or query better and would aid in a deeper understanding. Respond with each question in JSON format like 1: Question. Do not write any other text except the json "
    return

#Refine the ask by asking <number> of clarifying quesitons
def refine_llm(llm_0_url, llm_0_key, llm_0_model, llm_0, n_q,query):
    # ask LLM for set of X questions to clarify 
    LLM_QUERY="I will ask a question. Think deeply about 3 additional questions that could be asked that would help understand the problem or query better and would aid in a deeper understanding. Respond with each question in JSON format. Do not write any other text except the json. The question is: "+query
    json_results=llm_0(llm_0_url, llm_0_key,llm_0_model,LLM_QUERY)
    if json_results:
        response_hash={}
        for item in json.loads(json_results) :
            response_hash[item["response"]["id"]]=item["response"]["question"]
        #print(Fore.RED+"Questions to refine research: "+Style.RESET_ALL)
        print_red("Questions to refine research: ")
        for q in response_hash:
            print(response_hash[q])

# MAIN
def main():
    cli_args()
    if not cli_query:
        print("No query provided, use -q <query>")
        query="What is the greatest LLM"
    else:
        query=cli_query
        
    refine_llm(llm_0_url, llm_0_key, llm_0_model, llm_0, n_q,query)
    
if __name__ == "__main__":
    main()