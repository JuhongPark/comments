import json
import sqlite3

INPUT_FILE = "comments.json"
DB_FILE = "comments.db"

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        comments = json.load(f)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            cid TEXT PRIMARY KEY,
            text TEXT,
            time TEXT,
            author TEXT,
            channel TEXT,
            votes TEXT,
            photo TEXT,
            heart TEXT,
            reply TEXT,
            time_parsed TEXT,
            negative TEXT,
            angry TEXT,
            spam TEXT,
            response TEXT
        )
    """)

    for comment in comments:
        cursor.execute("""
            INSERT OR IGNORE INTO comments
            (cid, text, time, author, channel, votes, photo, heart, reply, time_parsed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            str(comment.get("cid", "")),
            str(comment.get("text", "")),
            str(comment.get("time", "")),
            str(comment.get("author", "")),
            str(comment.get("channel", "")),
            str(comment.get("votes", "")),
            str(comment.get("photo", "")),
            str(comment.get("heart", "")),
            str(comment.get("reply", "")),
            str(comment.get("time_parsed", "")),
        ))

    conn.commit()
    total = cursor.execute('SELECT COUNT(*) FROM comments').fetchone()[0]
    print(f"{DB_FILE} ready with {total} rows")
    conn.close()

if __name__ == "__main__":
    main()
