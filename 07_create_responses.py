import json
import sqlite3
import ollama

MODEL = "gemma3:1b-it-qat"
DB_FILE = "comments.db"
BATCH_SIZE = 100

def generate_batch_responses(batch):
    comments_block = "\n".join(f'{cid}: "{text[:150]}"' for cid, text in batch)
    response = ollama.chat(
        model=MODEL,
        messages=[{
            "role": "user",
            "content": f"Write a brief polite response for each YouTube comment below. "
                       f"Return JSON object mapping comment ID to response string.\n\n"
                       f"{comments_block}\n\n"
                       f"JSON format: {{\"cid1\": \"response1\", \"cid2\": \"response2\", ...}}"
        }],
        format="json",
        options={"num_predict": 2000},
    )
    try:
        return json.loads(response["message"]["content"])
    except (json.JSONDecodeError, KeyError):
        return {}

def main():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        cursor.execute("ALTER TABLE comments ADD COLUMN responses TEXT")
    except sqlite3.OperationalError:
        pass

    cursor.execute(
        "SELECT cid, text FROM comments "
        "WHERE LOWER(TRIM(response)) IN ('true', 'yes', '1') "
        "AND (responses IS NULL OR responses = '')"
    )
    rows = cursor.fetchall()

    if not rows:
        print("No comments need responses.")
        conn.close()
        return

    print(f"Generating responses for {len(rows)} comments in batches of {BATCH_SIZE}...")

    total_generated = 0
    for i in range(0, len(rows), BATCH_SIZE):
        batch = rows[i:i + BATCH_SIZE]
        results = generate_batch_responses(batch)

        for cid, text in batch:
            resp = results.get(cid, results.get(str(cid), "Thank you for your comment!"))
            cursor.execute("UPDATE comments SET responses = ? WHERE cid = ?", (str(resp), cid))
            total_generated += 1

        conn.commit()
        print(f"  Batch {i // BATCH_SIZE + 1}: {min(i + BATCH_SIZE, len(rows))}/{len(rows)} done", flush=True)

    conn.close()
    print(f"Generated responses for {total_generated} comments")

if __name__ == "__main__":
    main()
