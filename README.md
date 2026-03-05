# YouTube Comment Analysis and Moderation

Analyze and moderate YouTube comments using LLM classification and prompt engineering.

## Video
[Sam Altman: OpenAI CEO on GPT-4, ChatGPT, and the Future of AI](https://www.youtube.com/watch?v=L_Guz73e6fw)

## Pipeline

| Step | Script | Output |
|------|--------|--------|
| Install requirements | setup_requirements.py | - |
| Extract comments | 01_extract.py | comments.json |
| Count comments | 02_count.py | - |
| Create database | 03_database.py | comments.db |
| Sample data | sample_data.json, prompt.txt | - |
| Ping LLM | 05_ping_llm.py | - |
| Classify comments | 06_prediction.py | comments.db (updated) |
| Generate responses | 07_create_responses.py | comments.db (updated) |
| Extract categories | 08_categories.py | categories.json |
| Visualize clusters | 09_visualization.py | clusters.png |
| Export dataset | 11_export.py | clean_dataset.json |
| Run full pipeline | 12_pipeline.py | all of the above |

## Model Selection

Using **gemma3:270m** via Ollama. Initially tested gemma3:1b (larger model), but found that both models struggle with classification accuracy without good prompts. On a 2-core Codespace environment, the smaller model runs significantly faster while achieving comparable results when paired with a well-engineered prompt. This led to a strategy shift: **prompt engineering matters more than model size** for this classification task.

## Prompt Engineering

Tested 10 prompt variations on the first 100 comments (see `prompts/` folder). Key findings:
- Too many few-shot examples cause the small model to over-trigger or copy the first example
- Explicit "NOT negative" rules for praise/jokes prevent false positives
- Defining response detection via "?" question marks gives clearer signal than vague definitions
- Best result: prompt_v9 — negative ~18%, angry/spam/response at low single digits

## Problem Set
[Project Specification](https://docs.google.com/document/d/18yhShGNCJ5BGsRysKhnlyAdCk53sn-gW2_Vb2eZUKPE/edit?usp=sharing)
