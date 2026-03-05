import json
import sqlite3
import ollama

MODEL = "gemma3:270m"
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
            "content": f"Task: categorize these YouTube comments into themes.\n\n"
                       f"{comments_block}\n\n"
                       f"Return JSON with multiple categories:\n"
                       f'{{"categories": ['
                       f'{{"name": "Praise", "description": "Positive feedback about the interview", "count": 5}}, '
                       f'{{"name": "AI Ethics", "description": "Comments about ethical concerns of AI", "count": 3}}, '
                       f'{{"name": "Criticism", "description": "Negative or hostile comments", "count": 2}}, '
                       f'{{"name": "Questions", "description": "Comments asking questions or seeking clarification", "count": 4}}, '
                       f'{{"name": "Spam", "description": "Promotional or off-topic comments", "count": 1}}'
                       f']}}\n\n'
                       f"Now categorize all the comments above. Return at least 3 categories:"
        }],
        format="json",
    )

    try:
        result = json.loads(response["message"]["content"])
    except json.JSONDecodeError:
        result = {"categories": [], "raw": response["message"]["content"]}

    with open("categories.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"\nCategories saved to categories.json")

if __name__ == "__main__":
    main()
