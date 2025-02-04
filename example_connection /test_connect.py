from dotenv import load_dotenv
from openai import OpenAI
import os
#Setup creds 
load_dotenv()

client = OpenAI(
	base_url="https://openrouter.ai/api/v1",
	api_key=os.getenv("OPENROUTER_API_KEY")
)
query="What is the best sport to play"
LLM_QUERY="I will ask a question. Think deeply about 3 additional questions that could be asked that would help understand the problem or query better and would aid in a deeper understanding. Respond with each question in JSON format like 1: Question. Do not write any other text except the json. The question is: "+query
messages = [
	{
		"role": "developer",
		"content": "You are a helpful research assistant. Always respond in the following JSON format: [{\"response\": {\"id\": 1,\"question\": \"Some type of question\"}}, {\"response\": {\"id\": 2,\"question\": \"Some type of question\"}}]. Do not include any extra text, explanations, or variations in formatting."
	},
	{
		"role": "user",
		"content": LLM_QUERY
	}
]

completion = client.chat.completions.create(
	model="meta-llama/llama-3.2-3b-instruct:free", 
	messages=messages, 
	max_tokens=500
)

print(completion.choices[0].message.content)
