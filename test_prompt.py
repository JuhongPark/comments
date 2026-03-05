import json
import sqlite3
import sys
import ollama

MODEL = "gemma3:270m"
DB_FILE = "comments.db"
MAX_RETRIES = 2
DEFAULT = {"angry": False, "negative": False, "response": False, "spam": False}


def normalize_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in ("true", "yes", "1")
    return bool(value)


def classify(text, prompt_template):
    prompt = prompt_template.replace("{comment}", text)
    for attempt in range(MAX_RETRIES):
        try:
            resp = ollama.chat(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                format="json",
                options={"temperature": 0.3, "num_predict": 30},
            )
            raw = json.loads(resp["message"]["content"])
            return {k: normalize_bool(raw.get(k, False)) for k in DEFAULT}
        except (json.JSONDecodeError, KeyError):
            continue
    return dict(DEFAULT)


def main():
    prompt_file = sys.argv[1] if len(sys.argv) > 1 else "prompt.txt"
    with open(prompt_file, "r") as f:
        prompt_template = f.read()

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT cid, text FROM comments ORDER BY rowid LIMIT 100")
    rows = c.fetchall()
    conn.close()

    results = []
    for i, (cid, text) in enumerate(rows):
        r = classify(text, prompt_template)
        results.append(r)
        if (i + 1) % 25 == 0:
            print(f"  {i+1}/100...", flush=True)

    # Stats
    total = len(results)
    counts = {k: sum(1 for r in results if r[k]) for k in DEFAULT}

    print(f"\n{'='*50}")
    print(f"Prompt: {prompt_file}")
    print(f"Model: {MODEL} | Comments: {total}")
    print(f"{'='*50}")
    for k, v in counts.items():
        print(f"  {k:>10}: {v:>3}/{total}  ({v*100//total}%)")
    print(f"{'='*50}")

    # Show some examples where response=true
    print(f"\nSample response=true comments:")
    resp_true = [(rows[i][1], results[i]) for i in range(total) if results[i]["response"]]
    for text, r in resp_true[:5]:
        print(f"  - {text[:80]}  {r}")

    print(f"\nSample response=false comments:")
    resp_false = [(rows[i][1], results[i]) for i in range(total) if not results[i]["response"]]
    for text, r in resp_false[:5]:
        print(f"  - {text[:80]}  {r}")


if __name__ == "__main__":
    main()
