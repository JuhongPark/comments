# clean_dataset.json Structure Documentation
#
# File format: JSON with two top-level keys: "metadata" and "data"
#
# Columns:
#   cid        (string) - Unique comment ID from YouTube
#   text       (string) - Comment text content
#   time       (string) - Relative time string (e.g. "2 years ago")
#   author     (string) - Comment author name
#   channel    (string) - Author YouTube channel ID
#   votes      (string) - Number of likes on the comment
#   photo      (string) - Author profile photo URL
#   heart      (string) - Whether the comment received a creator heart
#   reply      (string) - Whether this comment is a reply to another comment
#   time_parsed(string) - Parsed Unix timestamp
#   negative   (string) - LLM classification: negative sentiment (True/False)
#   angry      (string) - LLM classification: angry tone (True/False)
#   spam       (string) - LLM classification: spam content (True/False)
#   response   (string) - LLM classification: needs response (True/False)
#   responses  (string) - Generated response text (null if not applicable)
#
# Assumptions and Decisions:
#   - Classification results (negative, angry, spam, response) are LLM predictions
#     using gemma3:1b-it-qat and may contain misclassifications.
#   - All field values are stored as strings because SQLite does not enforce strict
#     typing. Boolean classifications are stored as "True"/"False" strings.
#   - The "response" field is primarily determined by whether the comment contains
#     a question mark ("?"), as this was the most reliable signal for the small model.
#   - Comments are a point-in-time snapshot. New comments or deleted comments on
#     the video are not reflected in this dataset.
#   - The "responses" column is only populated for comments where response=True.
#     All other comments have null for this field.

import json
import sqlite3

DB_FILE = "comments.db"
OUTPUT_FILE = "clean_dataset.json"

def main():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM comments")
    rows = cursor.fetchall()

    columns = [description[0] for description in cursor.description]

    column_descriptions = {
        "cid": {"type": "string", "description": "Unique comment ID"},
        "text": {"type": "string", "description": "Comment text content"},
        "time": {"type": "string", "description": "Relative time string"},
        "author": {"type": "string", "description": "Comment author name"},
        "channel": {"type": "string", "description": "Author YouTube channel ID"},
        "votes": {"type": "string", "description": "Number of likes"},
        "photo": {"type": "string", "description": "Author profile photo URL"},
        "heart": {"type": "string", "description": "Whether comment received a creator heart"},
        "reply": {"type": "string", "description": "Whether this is a reply"},
        "time_parsed": {"type": "string", "description": "Parsed timestamp"},
        "negative": {"type": "string", "description": "LLM classification: negative sentiment"},
        "angry": {"type": "string", "description": "LLM classification: angry tone"},
        "spam": {"type": "string", "description": "LLM classification: spam content"},
        "response": {"type": "string", "description": "LLM classification: needs response"},
        "responses": {"type": "string", "description": "Generated response text"},
    }

    dataset = {
        "metadata": {
            "description": "Clean formatted dataset exported from comments.db",
            "total_records": len(rows),
            "columns": {col: column_descriptions[col] for col in columns if col in column_descriptions},
            "assumptions": [
                "Classification results are LLM predictions using gemma3:1b-it-qat and may contain misclassifications",
                "All values are stored as strings due to SQLite's flexible typing. Boolean fields use 'True'/'False' strings",
                "The response field is primarily based on question mark presence, as this was the most reliable signal for the model",
                "Comments are a point-in-time snapshot and may not reflect current state of the video",
                "The responses column is only populated for comments where response=True",
            ]
        },
        "data": [dict(row) for row in rows]
    }

    conn.close()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    print(f"Exported {len(rows)} records to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
