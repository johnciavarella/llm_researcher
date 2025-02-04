#!/usr/bin/python3
import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI
import json
import re
from colorama import Fore, Back, Style #Colors
from datetime import datetime
#Setup creds 
load_dotenv() #Get creds from .env 
pref_d = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

llm_0_url=os.getenv("Q_URL_ENDPOINT")
llm_0_key=os.getenv("OPENROUTER_API_KEY")
llm_0_model=os.getenv("Q_MODEL")

llm_1_url=os.getenv("R_URL_ENDPOINT")
llm_1_key=os.getenv("OPENROUTER_API_KEY")
llm_1_model=os.getenv("R_MODEL")

llm_2_url=os.getenv("S_URL_ENDPOINT")
llm_2_key=os.getenv("OPENROUTER_API_KEY")
llm_2_model=os.getenv("S_MODEL")

global total_summary
total_summary=""

# Set vars 
def cli_args():
    global debug_mode
    global o_dir
    global o_file
    global cli_query
    global n_q
    global n_refine
    parser = argparse.ArgumentParser(description="Script with debug flag")
    parser.add_argument("-q",#required=True,
                        help="Question to research")
    parser.add_argument("-n_q",default="3",help="N of questions to answer (first refine)")
    parser.add_argument("-n_refine",type=int,default="3",help="N of refinement iterations")
    parser.add_argument("-o_dir",default="research/",help="Output Directory")
    parser.add_argument("-o_file",default="Research",help="Outputfile")
    parser.add_argument("-debug",action="store_true",help="Debug Mode",)
    args = parser.parse_args()

    cli_query = args.q
    n_q = args.n_q
    n_refine = args.n_refine
    o_file = args.o_file
    o_dir = args.o_dir
    debug_mode = args.debug
    return cli_query, n_q, n_refine, o_file, o_dir

#Pretty
def print_red(x):print(Fore.RED+x+Style.RESET_ALL)
def print_cyan(x):print(Fore.CYAN+x+Style.RESET_ALL)

#outputter
def write_disk(content):
    #total_summary=total_summary
    #total_summary=total_summary+"\n\n\n"+total_summary
    if not os.path.exists(o_dir):
        os.makedirs(o_dir)   
    with open(o_dir+pref_d+"-"+o_file+".md", "a") as file:
        file.write(content + "\n")

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
        max_tokens=4500)
    
    json_results=completion.choices[0].message.content
    return json_results

def llm_1(llm_1_url,llm_1_key,llm_1_model,q):
    client = OpenAI(
        base_url=llm_1_url,
        api_key=llm_1_key)

    messages = [{
                "role": "developer",
                "content": "Problem Statement: Meticulously organize and analyze the provided question to extract valuable insights, enhance clarity, and add explanations where necessary.  Instructions:  1. Input: Please consider the question to organize and analyze before processing. 2. Preparation: Familiarize yourself with the context, themes, and objectives of each piece. This will help you effectively organize and analyze them.  3. Organizational Structure: Create a logical structure for your analysis based on genres, authors, themes, or other relevant criteria.  4. Thorough Examination: Dive deep into each piece of information, extract valuable insights, and note important quotes, passages, or ideas.  5. Add Explanations: If needed, add explanations to clarify complex concepts or provide additional context.  6. Identify Themes: Identify recurring themes, motifs, or ideas within the question. Highlight connections between different pieces.  7. Critical Analysis: Offer critical analysis and interpretations, evaluating the strengths, weaknesses, and significance of individual works.  8. Synthesis: Synthesize your findings into a cohesive analysis, ensuring a logical flow between paragraphs and sections.  9. Promote Creativity: Infuse your analysis with creativity, engaging language, and thought-provoking interpretations.  10. Utilize NLP Techniques: Leverage natural language processing techniques such as sentiment analysis, language modeling, and word embeddings to enhance your analysis.  11. Engage with the Question: Actively interact with the question asked, ask questions, and make revisions to refine your analysis.  12. Be Transparent: Clearly explain the rationale behind your categorization, interpretations, and connections, aiming for accessibility to readers. The user will be unable to answer questions, so any information provided will be the end of the context"
                },
                {
                "role": "user",
                "content": q
                }]

    completion = client.chat.completions.create(
        model=llm_1_model, 
        messages=messages, 
        max_tokens=10000)
    
    json_results=completion.choices[0].message.content
    return json_results

def llm_2(llm_2_url,llm_2_key,llm_2_model,total_summary):
    client = OpenAI(
    base_url=llm_2_url,
    api_key=llm_2_key)

    messages = [{
                "role": "developer",
                "content": "Summarize the following large block of text by extracting the key points, main ideas, and essential details while removing redundancy. Ensure the summary is clear, concise, and retains the core message. Include a bulleted list for a quick and easy-to-read overview. Additionally, provide a few thought-provoking questions at the end to encourage further exploration of the topic. Length should be 1-3 paragraphs and 5-20 bullet points"
                },
                {
                "role": "user",
                "content": total_summary
                }]

    completion = client.chat.completions.create(
        model=llm_2_model, 
        messages=messages, 
        max_tokens=10000)
    
    json_results=completion.choices[0].message.content
    return json_results
    

def thought_loop():
    test=test
    return

#Refine the ask by asking <number> of clarifying quesitons
def refine_llm(llm_0_url, llm_0_key, llm_0_model,query,n_q):
    #Setup Var
    global refine_llm_hash
    refine_llm_hash={}
    # ask LLM for set of X questions to clarify 
    LLM_QUERY="I will ask a question. Think deeply about "+n_q+" additional questions that could be asked that would help understand the problem or query better and would aid in a deeper understanding. Respond with each question in JSON format. Do not write any other text except the json. The question is: "+query
    json_results=llm_0(llm_0_url, llm_0_key,llm_0_model,LLM_QUERY)
    if json_results:
        for item in json.loads(json_results):
            refine_llm_hash[item["response"]["id"]]=item["response"]["question"]
        print_red("Questions to refine research: ")
        for q in refine_llm_hash:
            print_cyan(refine_llm_hash[q])
    return refine_llm_hash

#Research
def research_llm(llm_1_url, llm_1_key, llm_1_model,q):
    #Setup Var
    global research_llm_hash
    research_llm_hash={}
    # ask LLM for set of X questions to clarify 
    LLM_QUERY=q
    print_red(q)
    llm_output=llm_1(llm_1_url, llm_1_key, llm_1_model,LLM_QUERY)
    print(llm_output)
    write_disk(llm_output)
    # ToDo - Add saving to mem to reuse
    return research_llm_hash

#Summarize
def summarize_llm(llm_2_url, llm_2_key, llm_2_model, llm_2):
    # ask LLM to summarize 
    print_red(total_summary)
    summary=llm_2(llm_2_url, llm_2_key, llm_2_model,total_summary)
    print(f"# Summary: \n\n"+summary)
    write_disk(summary)
    # ToDo - Add saving to mem to reuse
    return summary 

# MAIN
def main():
    cli_args()
    
    if not cli_query:
        print("No query provided, use -q <query>")
        query="What is the greatest LLM"
    else:
        query=cli_query
        
    refine_llm(llm_0_url, llm_0_key, llm_0_model,query,n_q)
    
    #Record Metadata  
    write_disk(f"Generating Query: {query}\n\nModel_Refine: {llm_0_model} \n Model_Research: {llm_1_model} \n\n")
    
    for q in refine_llm_hash:
        #print(refine_llm_hash[q]) #Redundant as it is now printed in the function 
        if o_dir or o_file:
            write_disk(f"# Question: {refine_llm_hash[q]}\n\n")
        research_llm(llm_1_url, llm_1_key, llm_1_model,refine_llm_hash[q])
    #summarize_llm(llm_2_url, llm_2_key, llm_2_model, total_summary)
    
if __name__ == "__main__":
    main()
    