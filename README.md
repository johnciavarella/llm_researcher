# LLM Researcher 

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


## Useage 

```
python3 loopy.py -q "Query"
```