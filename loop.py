#!/usr/bin/python3
import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI
import json
from colorama import Fore, Back, Style
from datetime import datetime

class LLMConfig:
    """Configuration class for LLM settings."""
    def __init__(self, url: str, key: str, model: str):
        self.url = url
        self.key = key
        self.model = model

def load_config() -> dict[str, LLMConfig]:
    """Load LLM configurations from environment variables."""
    load_dotenv()
    configs = {
        'llm_0': LLMConfig(
            os.getenv("Q_URL_ENDPOINT"),
            os.getenv("OPENROUTER_API_KEY"),
            os.getenv("Q_MODEL")
        ),
        'llm_1': LLMConfig(
            os.getenv("R_URL_ENDPOINT"),
            os.getenv("OPENROUTER_API_KEY"),
            os.getenv("R_MODEL")
        ),
        'llm_2': LLMConfig(
            os.getenv("S_URL_ENDPOINT"),
            os.getenv("OPENROUTER_API_KEY"),
            os.getenv("S_MODEL")
        )
    }
    return configs

class Args:
    """Command line arguments container."""
    def __init__(self, cli_query: str | None, n_q: str, n_refine: int, 
                 o_file: str, o_dir: str, debug_mode: bool):
        self.cli_query = cli_query
        self.n_q = n_q
        self.n_refine = n_refine
        self.o_file = o_file
        self.o_dir = o_dir
        self.debug_mode = debug_mode

def cli_args() -> Args:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Script with debug flag")
    parser.add_argument("-q", help="Question to research")
    parser.add_argument("-n_q", default="3", help="N of questions to answer (first refine)")
    parser.add_argument("-n_refine", type=int, default="3", help="N of refinement iterations")
    parser.add_argument("-o_dir", default="research/", help="Output Directory")
    parser.add_argument("-o_file", default="Research", help="Outputfile")
    parser.add_argument("-debug", action="store_true", help="Debug Mode")
    args = parser.parse_args()

    return Args(
        args.q,
        args.n_q,
        args.n_refine,
        args.o_file,
        args.o_dir,
        args.debug
    )

def print_red(x): print(Fore.RED + x + Style.RESET_ALL)
def print_cyan(x): print(Fore.CYAN + x + Style.RESET_ALL)

def write_disk(content: str, args: Args) -> None:
    """Write content to disk with timestamp."""
    pref_d = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if not os.path.exists(args.o_dir):
        os.makedirs(args.o_dir)   
    with open(args.o_dir + pref_d + "-" + args.o_file + ".md", "a") as file:
        file.write(content + "\n")

def llm_0(config: LLMConfig, query: str) -> str:
    """Generate questions using LLM to refine research."""
    client = OpenAI(
        base_url=config.url,
        api_key=config.key)

    messages = [{
                "role": "developer",
                "content": "You are a helpful research assistant. Always respond in the following JSON format: [{\"response\": {\"id\": 1,\"question\": \"Some type of question\"}}, {\"response\": {\"id\": 2,\"question\": \"Some type of question\"}}]. Do not include any extra text, explanations, or variations in formatting."
                },
                {
                "role": "user",
                "content": query
                }]

    completion = client.chat.completions.create(
        model=config.model, 
        messages=messages, 
        max_tokens=4500)
    
    return completion.choices[0].message.content

def llm_1(config: LLMConfig, q: str) -> str:
    """Process and analyze questions using LLM."""
    client = OpenAI(
        base_url=config.url,
        api_key=config.key)

    messages = [{
                "role": "developer",
                "content": "Problem Statement: Meticulously organize and analyze the provided question to extract valuable insights, enhance clarity, and add explanations where necessary.  Instructions:  1. Input: Please consider the question to organize and analyze before processing. 2. Preparation: Familiarize yourself with the context, themes, and objectives of each piece. This will help you effectively organize and analyze them.  3. Organizational Structure: Create a logical structure for your analysis based on genres, authors, themes, or other relevant criteria.  4. Thorough Examination: Dive deep into each piece of information, extract valuable insights, and note important quotes, passages, or ideas.  5. Add Explanations: If needed, add explanations to clarify complex concepts or provide additional context.  6. Identify Themes: Identify recurring themes, motifs, or ideas within the question. Highlight connections between different pieces.  7. Critical Analysis: Offer critical analysis and interpretations, evaluating the strengths, weaknesses, and significance of individual works.  8. Synthesis: Synthesize your findings into a cohesive analysis, ensuring a logical flow between paragraphs and sections.  9. Promote Creativity: Infuse your analysis with creativity, engaging language, and thought-provoking interpretations.  10. Utilize NLP Techniques: Leverage natural language processing techniques such as sentiment analysis, language modeling, and word embeddings to enhance your analysis.  11. Engage with the Question: Actively interact with the question asked, ask questions, and make revisions to refine your analysis.  12. Be Transparent: Clearly explain the rationale behind your categorization, interpretations, and connections, aiming for accessibility to readers. The user will be unable to answer questions, so any information provided will be the end of the context"
                },
                {
                "role": "user",
                "content": q
                }]

    completion = client.chat.completions.create(
        model=config.model, 
        messages=messages, 
        max_tokens=10000)
    
    return completion.choices[0].message.content

def llm_2(config: LLMConfig, total_summary: str) -> str:
    """Generate summary using LLM."""
    client = OpenAI(
        base_url=config.url,
        api_key=config.key)

    messages = [{
                "role": "developer",
                "content": "Summarize the following large block of text by extracting the key points, main ideas, and essential details while removing redundancy. Ensure the summary is clear, concise, and retains the core message. Include a bulleted list for a quick and easy-to-read overview. Additionally, provide a few thought-provoking questions at the end to encourage further exploration of the topic. Length should be 1-3 paragraphs and 5-20 bullet points"
                },
                {
                "role": "user",
                "content": total_summary
                }]

    completion = client.chat.completions.create(
        model=config.model, 
        messages=messages, 
        max_tokens=10000)
    
    return completion.choices[0].message.content

def refine_llm(config: LLMConfig, query: str, n_q: str) -> dict[int, str]:
    """Generate and return refinement questions."""
    LLM_QUERY = "I will ask a question. Think deeply about " + n_q + " additional questions that could be asked that would help understand the problem or query better and would aid in a deeper understanding. Respond with each question in JSON format. Do not write any other text except the json. The question is: " + query
    json_results = llm_0(config, LLM_QUERY)
    
    refine_llm_hash = {}
    if json_results:
        for item in json.loads(json_results):
            refine_llm_hash[item["response"]["id"]] = item["response"]["question"]
        print_red("Questions to refine research: ")
        for q in refine_llm_hash:
            print_cyan(refine_llm_hash[q])
    return refine_llm_hash

def research_llm(config: LLMConfig, q: str, args: Args) -> str:
    """Research a specific question and return findings."""
    LLM_QUERY = q
    print_red(q)
    llm_output = llm_1(config, LLM_QUERY)
    print(llm_output)
    write_disk(llm_output, args)
    return llm_output

def summarize_llm(config: LLMConfig, total_summary: str, args: Args) -> str:
    """Generate and return a summary of all research."""
    print_cyan(total_summary)
    summary = llm_2(config, total_summary)
    print(f"# Summary: \n\n" + summary)
    write_disk(summary, args)
    return summary

def main() -> None:
    """Main execution flow."""
    args = cli_args()
    configs = load_config()
    
    query = "What is the greatest LLM" if not args.cli_query else args.cli_query
    
    if args.debug_mode:
        print(f"Query: {query}")
        print(f"Models: {configs['llm_0'].model}, {configs['llm_1'].model}, {configs['llm_2'].model}")
    
    refine_hash = refine_llm(configs['llm_0'], query, args.n_q)
    
    write_disk(
        f"Generating Query: {query}\n\nModel_Refine: {configs['llm_0'].model} \n Model_Research: {configs['llm_1'].model} \n\n",
        args
    )
    
    total_summary = ""
    for q in refine_hash:
        if args.o_dir or args.o_file:
            write_disk(f"# Question: {refine_hash[q]}\n\n", args)
        output = research_llm(configs['llm_1'], refine_hash[q], args)
        total_summary += output + "\n\n"
    
    if total_summary:
        summarize_llm(configs['llm_2'], total_summary, args)

if __name__ == "__main__":
    main()
