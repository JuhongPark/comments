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

    dataset = {
        "metadata": {
            "description": "Clean formatted dataset exported from comments.db",
            "total_records": len(rows),
            "columns": {
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
            },
            "assumptions": [
                "All classification fields are populated by LLM predictions",
                "Responses are generated only for comments flagged as needing a response",
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
