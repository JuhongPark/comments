import json
import sqlite3

DB_FILE = "comments.db"

def main():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM comments")
    total = cursor.fetchone()[0]

    # Build categories from classification data
    categories = []

    # Count negative comments
    cursor.execute("SELECT COUNT(*) FROM comments WHERE LOWER(TRIM(negative)) IN ('true', 'yes', '1')")
    neg_count = cursor.fetchone()[0]
    if neg_count > 0:
        categories.append({
            "name": "Criticism",
            "description": "Negative or disapproving comments",
            "count": neg_count
        })

    # Count angry comments
    cursor.execute("SELECT COUNT(*) FROM comments WHERE LOWER(TRIM(angry)) IN ('true', 'yes', '1')")
    angry_count = cursor.fetchone()[0]
    if angry_count > 0:
        categories.append({
            "name": "Angry",
            "description": "Hostile or aggressive comments",
            "count": angry_count
        })

    # Count spam comments
    cursor.execute("SELECT COUNT(*) FROM comments WHERE LOWER(TRIM(spam)) IN ('true', 'yes', '1')")
    spam_count = cursor.fetchone()[0]
    if spam_count > 0:
        categories.append({
            "name": "Spam",
            "description": "Promotional or off-topic comments",
            "count": spam_count
        })

    # Count comments needing response
    cursor.execute("SELECT COUNT(*) FROM comments WHERE LOWER(TRIM(response)) IN ('true', 'yes', '1')")
    resp_count = cursor.fetchone()[0]
    if resp_count > 0:
        categories.append({
            "name": "Questions",
            "description": "Comments that ask questions or need a reply",
            "count": resp_count
        })

    # Positive/neutral: comments with none of the above flags
    cursor.execute("""SELECT COUNT(*) FROM comments
        WHERE LOWER(TRIM(COALESCE(negative,''))) NOT IN ('true', 'yes', '1')
        AND LOWER(TRIM(COALESCE(angry,''))) NOT IN ('true', 'yes', '1')
        AND LOWER(TRIM(COALESCE(spam,''))) NOT IN ('true', 'yes', '1')
        AND LOWER(TRIM(COALESCE(response,''))) NOT IN ('true', 'yes', '1')
    """)
    neutral_count = cursor.fetchone()[0]
    if neutral_count > 0:
        categories.append({
            "name": "Praise",
            "description": "Positive or neutral feedback about the content",
            "count": neutral_count
        })

    conn.close()

    result = {"categories": categories}

    with open("categories.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"\nCategories saved to categories.json")

if __name__ == "__main__":
    main()
