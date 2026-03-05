import json
import sqlite3
import ollama

MODEL = "llama3.2:3b"
DB_FILE = "comments.db"

def main():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT text FROM comments")
    rows = cursor.fetchall()
    conn.close()

    # Sample comments for category analysis (use up to 100)
    sample_texts = [row[0] for row in rows[:100]]
    comments_block = "\n".join([f"- {text}" for text in sample_texts])

    response = ollama.chat(
        model=MODEL,
        messages=[{
            "role": "user",
            "content": f"Analyze these YouTube comments and identify the main thematic categories. "
                       f"For each category, provide its name, description, and approximate count.\n\n"
                       f"Respond in JSON format:\n"
                       f'{{"categories": [{{"name": "...", "description": "...", "count": N}}]}}\n\n'
                       f"Comments:\n{comments_block}"
        }],
        format="json",
    )

    try:
        result = json.loads(response["message"]["content"])
    except json.JSONDecodeError:
        result = {"categories": [], "raw": response["message"]["content"]}

    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
