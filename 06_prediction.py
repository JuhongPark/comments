import json
import sqlite3
import sys
import ollama

MODEL = "gemma3:1b"
DB_FILE = "comments.db"
PROMPT_FILE = "prompt.txt"
MAX_RETRIES = 2
BATCH_COMMIT_SIZE = 50
DEFAULT = {"angry": False, "negative": False, "response": False, "spam": False}

def normalize_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in ("true", "yes", "1")
    return bool(value)

def classify_comment(comment_text, prompt_template):
    prompt = prompt_template.replace("{comment}", comment_text)
    for attempt in range(MAX_RETRIES):
        try:
            response = ollama.chat(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                format="json",
                options={"temperature": 0.5, "num_predict": 30},
            )
            raw = json.loads(response["message"]["content"])
            return {k: normalize_bool(raw.get(k, False)) for k in DEFAULT}
        except (json.JSONDecodeError, KeyError):
            if attempt < MAX_RETRIES - 1:
                continue
    return dict(DEFAULT)

def main():
    # --reclassify flag: force reclassification of all comments (use after model change)
    reclassify = "--reclassify" in sys.argv

    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        prompt_template = f.read()

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    if reclassify:
        cursor.execute("SELECT cid, text FROM comments ORDER BY rowid")
        print("Reclassifying all comments (--reclassify flag set)...")
    else:
        cursor.execute("SELECT cid, text FROM comments WHERE negative IS NULL OR negative = '' ORDER BY rowid")

    rows = cursor.fetchall()

    if not rows:
        print("All comments already classified. Use --reclassify to force reclassification (e.g. after model change).")
        conn.close()
        return

    print(f"Classifying {len(rows)} comments...")

    for i, (cid, text) in enumerate(rows):
        result = classify_comment(text, prompt_template)
        cursor.execute("""
            UPDATE comments
            SET negative = ?, angry = ?, spam = ?, response = ?
            WHERE cid = ?
        """, (
            str(result["negative"]),
            str(result["angry"]),
            str(result["spam"]),
            str(result["response"]),
            cid
        ))
        if (i + 1) % BATCH_COMMIT_SIZE == 0:
            conn.commit()
            print(f"  Processed {i + 1}/{len(rows)} comments")

    conn.commit()
    conn.close()
    print(f"Updated {len(rows)} comments in database")

if __name__ == "__main__":
    main()
