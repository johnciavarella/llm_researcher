import os
from dotenv import load_dotenv
from openai import OpenAI

#Setup creds 
load_dotenv()
#llm_0_url="https://openrouter.ai/api/v1"
llm_0_url="https://api.groq.com/openai/v1"
llm_0_key=os.getenv("OPENROUTER_API_KEY")
#llm_0_model="google/gemini-2.0-flash-thinking-exp-1219:free"
llm_0_model="llama-3.1-8b-instant"

# llm_<num>_<obj> format for additonal models and API endpoints if desired 
#llm_0_url="https://openrouter.ai/api/v1"
#llm_0_key=os.getenv("OPENROUTER_API_KEY")
#llm_0_model="deepseek-ai/DeepSeek-R1"

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
                "role": "user",
                "content": query
                }]

    completion = client.chat.completions.create(
        model=llm_0_model, 
        messages=messages, 
        max_tokens=500)

    print(completion.choices[0].message.content)

# MAIN
def main():
    query="What is the first 10 digits of Pi"
    llm_0(llm_0_url, llm_0_key,llm_0_model,query)

if __name__ == "__main__":
    main()