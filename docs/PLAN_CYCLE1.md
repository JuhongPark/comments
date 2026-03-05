# Cycle 1 Plan

## Current State
- All 12 script files exist but are **empty** (0 bytes)
- All data files (comments.json, comments.db, clean_dataset.json, sample_data.json, prompt.txt) are **empty**
- Python 3.12.3, Ollama 0.17.0 available
- Ollama models: `gemma3:270m` (291 MB)
- No Python packages installed yet

## Task-by-Task Plan

### Task 1: `01_extract.py` → `comments.json`
- **Tool**: `youtube-comment-downloader` (pip install, no API key needed)
- **Approach**: Use Python API to fetch all comments from `https://www.youtube.com/watch?v=L_Guz73e6fw`
- **Output**: JSON array saved to `comments.json`
- **Fields expected**: cid, text, time, author, channel, votes, photo, heart, reply, time_parsed

### Task 2: `02_count.py`
- **Approach**: Load `comments.json`, count entries, print total
- **Output**: Print count to stdout

### Task 3: `03_database.py` → `comments.db`
- **Approach**: Read `comments.json`, create SQLite DB with `comments` table
- **Columns**: cid, text, time, author, channel, votes, photo, heart, reply, time_parsed + negative, angry, spam, response (4 new fields, default NULL)
- **Output**: `comments.db`

### Task 4: `sample_data.json` + `prompt.txt`
- **Approach**: Select 25 comments with mixed emotions from `comments.json`
- **prompt.txt**: Classification prompt that produces `{"angry": bool, "negative": bool, "response": bool, "spam": bool}`
- **Note**: This is a manual/curated task - select diverse comments

### Task 5: `05_ping_llm.py`
- **Approach**: Use `ollama` Python library to query model
- **Model**: `gemma3:270m` (only small model available)
- **Question**: "How many states are there in the United States of America?"
- **Output format**: `{"answer": "..."}`
- **Note**: Spec says `05_ping_llm.py` but pipeline list says `05_ping_openai.py` - existing file is `05_ping_openai.py`. Will use the existing filename.

### Task 6: `06_prediction.py`
- **Approach**: Load first 100 comments from DB, send each to Ollama for classification
- **Classify**: negative, angry, spam, response (true/false)
- **Update**: Write results back to `comments.db`
- **Model**: `gemma3:270m`

### Task 7: `07_create_responses.py`
- **Approach**: Add `responses` column to DB, generate LLM responses for comments where response=true
- **Store**: Responses in new column

### Task 8: `08_categories.py`
- **Approach**: Use LLM to identify thematic categories across comments
- **Output**: Print categories and counts

### Task 9: `09_visualization.py`
- **Approach**: Use `sentence-transformers` for embeddings, `scikit-learn` for K-means (5 clusters), t-SNE for 2D reduction
- **Visualization**: Matplotlib scatter plot with color-coded clusters and centroids
- **Output**: Plot saved as image file

### Task 10: `requirements.txt` + `setup_requirements.py`
- **requirements.txt**: List all packages used
- **setup_requirements.py**: `install_requirements()` function using `subprocess.check_call`

### Task 11: `11_export.py` → `clean_dataset.json`
- **Approach**: Read entire `comments.db`, export to formatted JSON
- **Include**: Column descriptions, data types documentation

### Task 12: `12_pipeline.py`
- **Approach**: Run all scripts sequentially using `subprocess`
- **Order**: setup_requirements → 01_extract → 02_count → 03_database → (sample_data) → 05_ping_openai → 06_prediction → 07_create_responses → 08_categories → 09_visualization → 11_export
- **Error handling**: Try/except with logging per step

## Dependencies (pip install)
- youtube-comment-downloader
- ollama
- sentence-transformers
- scikit-learn
- matplotlib
- numpy

## Resolved Questions
1. **Filename**: Using `05_ping_llm.py` (matches spec Task 5). Renamed from `05_ping_openai.py`. Pipeline (Task 12) will reference `05_ping_llm.py`.
2. **Model**: Pulling `llama3.2:3b` for better classification quality. Will use this for Tasks 5, 6, 7, 8.
3. **Task 4**: `sample_data.json` and `prompt.txt` are data files, not scripts. Will create a script to generate sample_data.json programmatically. prompt.txt will be manually crafted.
