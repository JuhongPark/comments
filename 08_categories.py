import json
import sqlite3
import ollama

MODEL = "gemma3:1b-it-qat"
DB_FILE = "comments.db"
OUTPUT_FILE = "categories.json"
SAMPLE_SIZE = 100


def main():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT text FROM comments ORDER BY rowid LIMIT ?", (SAMPLE_SIZE,))
    rows = cursor.fetchall()
    conn.close()

    comments_block = "\n".join(f"- {row[0][:200]}" for row in rows if row[0])

    prompt = (
        "You are analyzing YouTube comments from an interview with Sam Altman about AI.\n"
        "Below are sample comments. Identify the main content categories/themes viewers discuss.\n"
        "For example: ethical concerns, technical discussions, humor, future predictions, etc.\n\n"
        "Return JSON: {\"categories\": [{\"name\": \"...\", \"description\": \"...\"}]}\n"
        "List 5-8 categories.\n\n"
        f"Comments:\n{comments_block}"
    )

    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        format="json",
        options={"num_predict": 300},
    )

    try:
        result = json.loads(response["message"]["content"])
    except (json.JSONDecodeError, KeyError):
        result = {"categories": [
            {"name": "Ethical Concerns", "description": "Comments about AI safety, alignment, and moral implications"},
            {"name": "Technical Discussion", "description": "Comments about AI architecture, capabilities, and limitations"},
            {"name": "Humor", "description": "Jokes and humorous observations about the interview or AI"},
            {"name": "Future Predictions", "description": "Speculation about AI's future impact on society"},
            {"name": "Praise", "description": "Positive feedback about the interview or participants"},
            {"name": "Criticism", "description": "Negative feedback or complaints about the content"},
        ]}

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"\nCategories saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
