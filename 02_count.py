import json

INPUT_FILE = "comments.json"

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        comments = json.load(f)

    print(f"Total number of comments: {len(comments)}")

if __name__ == "__main__":
    main()
