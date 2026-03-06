import json
import sqlite3
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import ollama

MODEL = "gemma3:270m"
DB_FILE = "comments.db"
MAX_WORKERS = 4
MAX_RETRIES = 2
BATCH_COMMIT_SIZE = 50
DEFAULT = {"angry": False, "negative": False, "response": False, "spam": False}

PROMPT_TEMPLATE = """Classify YouTube comment. JSON: {"angry":bool,"negative":bool,"response":bool,"spam":bool}

angry = insults, name-calling, hostility. Examples: "idiot", "clown", "sleazy", "crap", "stupid", "killed"
negative = unhappy, criticizing, complaining. NOT negative: praise, jokes, humor, excitement, observations
response = comment contains "?" (question mark) = true. No "?" = false.
spam = off-topic (not about AI/interview), self-promotion, links to other channels

"Love this!" -> {"angry":false,"negative":false,"response":false,"spam":false}
"Sam is so smart" -> {"angry":false,"negative":false,"response":false,"spam":false}
"He looks like hitman 😅" -> {"angry":false,"negative":false,"response":false,"spam":false}
"pioneer in vocal fry" -> {"angry":false,"negative":false,"response":false,"spam":false}
"What time?" -> {"angry":false,"negative":false,"response":true,"spam":false}
"Is this real?" -> {"angry":false,"negative":false,"response":true,"spam":false}
"His family safe though... right?" -> {"angry":false,"negative":true,"response":true,"spam":false}
"Did you not ask him about X?" -> {"angry":false,"negative":true,"response":true,"spam":false}
"Boring interview" -> {"angry":false,"negative":true,"response":false,"spam":false}
"sleazy sales man" -> {"angry":true,"negative":true,"response":false,"spam":false}
"Look at the CLOWN" -> {"angry":true,"negative":true,"response":false,"spam":false}
"He's full of crap!" -> {"angry":true,"negative":true,"response":false,"spam":false}
"Happy birthday!" -> {"angry":false,"negative":false,"response":false,"spam":true}
"Check my podcast http://link" -> {"angry":false,"negative":false,"response":false,"spam":true}

Comment: "{comment}"
"""


def normalize_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in ("true", "yes", "1")
    return bool(value)


def classify_comment(cid, comment_text, prompt_template):
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
            return (cid, {k: normalize_bool(raw.get(k, False)) for k in DEFAULT})
        except (json.JSONDecodeError, KeyError):
            if attempt < MAX_RETRIES - 1:
                continue
    return (cid, dict(DEFAULT))


def main():
    reclassify = "--reclassify" in sys.argv

    prompt_template = PROMPT_TEMPLATE

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    if reclassify:
        cursor.execute("SELECT cid, text FROM comments ORDER BY rowid")
        print("Reclassifying all comments (--reclassify flag set)...")
    else:
        cursor.execute("SELECT cid, text FROM comments ORDER BY rowid LIMIT 100")
        print("Classifying first 100 comments (use --reclassify for all)...")

    rows = cursor.fetchall()

    if not rows:
        print("No comments to classify.")
        conn.close()
        return

    print(f"Classifying {len(rows)} comments with {MAX_WORKERS} parallel workers...")

    completed = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(classify_comment, cid, text, prompt_template): cid
            for cid, text in rows
        }

        for future in as_completed(futures):
            cid, result = future.result()
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
            completed += 1
            if completed % BATCH_COMMIT_SIZE == 0 or completed == len(rows):
                conn.commit()
                print(f"  Processed {completed}/{len(rows)} comments")

    conn.commit()
    conn.close()
    print(f"Updated {len(rows)} comments in database")


if __name__ == "__main__":
    main()
