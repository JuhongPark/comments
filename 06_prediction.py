import json
import sqlite3
import ollama

MODEL = "gemma3:270m"
DB_FILE = "comments.db"
PROMPT_FILE = "prompt.txt"

def classify_comment(comment_text, prompt_template):
    prompt = prompt_template.replace("{comment}", comment_text)
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        format="json",
    )
    try:
        return json.loads(response["message"]["content"])
    except json.JSONDecodeError:
        return {"angry": False, "negative": False, "response": False, "spam": False}

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
            str(result.get("negative", False)),
            str(result.get("angry", False)),
            str(result.get("spam", False)),
            str(result.get("response", False)),
            cid
        ))
        conn.commit()
        if (i + 1) % 10 == 0:
            print(f"  Processed {i + 1}/{len(rows)} comments")

    conn.close()
    print(f"Updated {len(rows)} comments in database")

if __name__ == "__main__":
    main()
