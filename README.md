# LLM Researcher 

## Useage 

```
usage: loop.py [-h] [-q Q] [-n_q N_Q] [-n_refine N_REFINE] [-o_dir O_DIR] [-o_file O_FILE] [-debug]

Script with debug flag

options:
  -h, --help          show this help message and exit
  -q Q                Question to research
  -n_q N_Q            N of questions to answer (first refine)
  -n_refine N_REFINE  N of refinement iterations
  -o_dir O_DIR        Output Directory
  -o_file O_FILE      Outputfile
  -debug              Debug Mode
```

Environment and Models 
:   Create an .env file to setup API keys and models. 
:   Recommended models depend on your usecase. 
:   Works with Ollama (local models)


## Goals 

Enable recursive LLM searches + RAG to assist with understanding a concept. 

### Highlevel concept (Current):

```mermaid
graph TD;
    User_Query-->Expound_w_LLM;
    Expound_w_LLM-->SubProcess-LLM-Refinement;
    SubProcess-LLM-Refinement-->Expound_w_LLM;
    Expound_w_LLM-->Summarize;
    Summarize-->output.md;
```



### Highlevel concept (Future):

```mermaid
graph TD;
    User_Query-->Expound_w_LLM;
    Expound_w_LLM-->SubProcess-RAG-Web;
    Expound_w_LLM-->SubProcess-RAG-VectorDB;
    Expound_w_LLM-->SubProcess-LLM-Refinement;
    SubProcess-RAG-Web-->Expound_w_LLM;
    SubProcess-RAG-VectorDB-->Expound_w_LLM;
    SubProcess-LLM-Refinement-->Expound_w_LLM;
    Expound_w_LLM-->Answer/Hypothesis; 
```


