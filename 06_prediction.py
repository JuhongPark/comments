import json
import sqlite3
import ollama

MODEL = "gemma3:270m"
DB_FILE = "comments.db"
PROMPT_FILE = "prompt.txt"
MAX_RETRIES = 3
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
                options={"temperature": 0.5},
            )
            raw = json.loads(response["message"]["content"])
            return {k: normalize_bool(raw.get(k, False)) for k in DEFAULT}
        except (json.JSONDecodeError, KeyError):
            if attempt < MAX_RETRIES - 1:
                continue
    return dict(DEFAULT)

def main():
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        prompt_template = f.read()

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT cid, text FROM comments ORDER BY rowid")
    rows = cursor.fetchall()

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
        conn.commit()
        if (i + 1) % 10 == 0:
            print(f"  Processed {i + 1}/{len(rows)} comments")

    conn.close()
    print(f"Updated {len(rows)} comments in database")

if __name__ == "__main__":
    main()
