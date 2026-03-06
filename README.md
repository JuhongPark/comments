# LLM-Based YouTube Comment Analysis and Moderation

Analyze and moderate YouTube comments using LLM classification and prompt engineering.

## Clustering Visualization

Comments are converted to embeddings using a pre-trained sentence model, clustered with K-means (5 clusters), and projected to 2D with t-SNE. Each point is a comment, colored by cluster. Red X marks are cluster centroids.

![Clustering Visualization](clusters.png)

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

## Dataset Structure (clean_dataset.json)

| Column | Type | Description |
|--------|------|-------------|
| cid | string | Unique comment ID from YouTube |
| text | string | Comment text content |
| time | string | Relative time string (e.g. "2 years ago") |
| author | string | Comment author name |
| channel | string | Author YouTube channel ID |
| votes | string | Number of likes on the comment |
| photo | string | Author profile photo URL |
| heart | string | Whether the comment received a creator heart |
| reply | string | Whether this comment is a reply to another comment |
| time_parsed | string | Parsed Unix timestamp |
| negative | string | LLM classification: negative sentiment (True/False) |
| angry | string | LLM classification: angry tone (True/False) |
| spam | string | LLM classification: spam content (True/False) |
| response | string | LLM classification: needs response (True/False) |
| responses | string | Generated response text (null if not applicable) |

Assumptions and Decisions:
- Classification results are LLM predictions using gemma3:1b-it-qat and may contain misclassifications
- All values are stored as strings due to SQLite's flexible typing. Boolean fields use "True"/"False" strings
- The response field is primarily based on question mark ("?") presence, as this was the most reliable signal for the model
- Comments are a point-in-time snapshot and may not reflect the current state of the video
- The responses column is only populated for comments where response=True

## Model Selection

Tested multiple models via Ollama to find the best balance of accuracy and speed:

| Model | Size | Accuracy | Notes |
|-------|------|----------|-------|
| gemma3:270m | 270M | ~50% | Fast, but predicted all-False regardless of input |
| gemma3:1b | 1B | ~67% | Predicted almost all-True for every field |
| llama3.2:3b | 3B | ~80% | Good accuracy, but too slow for 2000+ comments |
| **gemma3:1b-it-qat** | **1B** | **85%** | **QAT variant with prompt optimization** |

Selected gemma3:1b-it-qat as the final model. Although smaller than llama3.2:3b, prompt optimization (10 iterations on 25-sample ground truth) compensated for the size difference, achieving 85% accuracy with significantly faster inference.

## Prompt Engineering

Tested 28 prompt variations for llama3.2:3b (v2-v29) and 10 prompt variations for gemma3:1b-it-qat (gemma3_1b-it-qat_v1-v10) against a 25-comment ground truth dataset (see `prompts/` folder).

Key findings for gemma3:1b-it-qat:
- "Default is false for all" framing dramatically reduced false positives (58% -> 74%)
- Specifying the video topic ("about an AI interview") helped the model understand context
- Explicit "NOT negative" rules for praise/jokes/ideas eliminated negative false positives
- Adding specific insult words (clown, sleazy, idiot, NOTHING, killed) helps angry detection
- Best prompt: prompt_gemma3_1b-it-qat_v3 (85% accuracy, zero false positives across all fields)
