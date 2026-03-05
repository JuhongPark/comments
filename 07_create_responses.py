import sqlite3
import ollama

MODEL = "gemma3:270m"
DB_FILE = "comments.db"

def generate_response(comment_text):
    response = ollama.chat(
        model=MODEL,
        messages=[{
            "role": "user",
            "content": f"Write a brief, polite response to this YouTube comment:\n\n"
                       f"\"{comment_text}\"\n\n"
                       f"Keep the response concise and professional."
        }],
    )
    return response["message"]["content"]

def main():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Add responses column if not exists
    try:
        cursor.execute("ALTER TABLE comments ADD COLUMN responses TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists

    cursor.execute("SELECT cid, text FROM comments WHERE LOWER(TRIM(response)) IN ('true', 'yes', '1')")
    rows = cursor.fetchall()

    print(f"Generating responses for {len(rows)} comments...")

    for i, (cid, text) in enumerate(rows):
        response_text = generate_response(text)
        cursor.execute("UPDATE comments SET responses = ? WHERE cid = ?", (response_text, cid))
        if (i + 1) % 5 == 0:
            print(f"  Processed {i + 1}/{len(rows)} comments")

    conn.commit()
    conn.close()
    print(f"Generated responses for {len(rows)} comments")

if __name__ == "__main__":
    main()
