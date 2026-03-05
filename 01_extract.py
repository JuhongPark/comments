import json
from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_POPULAR

VIDEO_URL = "https://www.youtube.com/watch?v=L_Guz73e6fw"
OUTPUT_FILE = "comments.json"

def main():
    downloader = YoutubeCommentDownloader()
    print(f"Fetching comments from: {VIDEO_URL}")

    comments = list(downloader.get_comments_from_url(VIDEO_URL, sort_by=SORT_BY_POPULAR))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(comments, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(comments)} comments to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
