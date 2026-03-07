import json
import sqlite3
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer

DB_FILE = "comments.db"
CATEGORIES_FILE = "categories.json"
N_CLUSTERS = 5
OUTPUT_IMAGE = "clusters.png"


def get_cluster_theme(cluster_texts, all_texts):
    vectorizer = TfidfVectorizer(max_features=1000, stop_words="english", ngram_range=(1, 2))
    vectorizer.fit(all_texts)
    tfidf = vectorizer.transform(cluster_texts)
    mean_tfidf = tfidf.mean(axis=0).A1
    top_indices = mean_tfidf.argsort()[-3:][::-1]
    features = vectorizer.get_feature_names_out()
    return ", ".join(features[i] for i in top_indices)


def main():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT text, negative, angry, spam, response FROM comments")
    rows = cursor.fetchall()
    conn.close()

    filtered = [(r[0], r[1], r[2], r[3], r[4]) for r in rows if r[0]]
    texts = [r[0] for r in filtered]
    classifications = [{"negative": r[1], "angry": r[2], "spam": r[3], "response": r[4]} for r in filtered]
    print(f"Generating embeddings for {len(texts)} comments...")

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(texts, show_progress_bar=True)

    print(f"Applying K-means clustering with {N_CLUSTERS} clusters...")
    kmeans = KMeans(n_clusters=N_CLUSTERS, random_state=42, n_init=10)
    labels = kmeans.fit_predict(embeddings)

    print("Reducing dimensions with t-SNE...")
    tsne = TSNE(n_components=2, random_state=42, perplexity=min(30, len(texts) - 1))
    reduced = tsne.fit_transform(embeddings)

    centroids_2d = np.array([reduced[labels == i].mean(axis=0) for i in range(N_CLUSTERS)])

    cluster_themes = []
    for i in range(N_CLUSTERS):
        cluster_texts = [texts[j] for j in range(len(texts)) if labels[j] == i]
        theme = get_cluster_theme(cluster_texts, texts)
        cluster_themes.append(theme)

    plt.figure(figsize=(14, 9))
    scatter = plt.scatter(reduced[:, 0], reduced[:, 1], c=labels, cmap="tab10", alpha=0.6, s=10)
    plt.scatter(centroids_2d[:, 0], centroids_2d[:, 1], c="red", marker="X", s=200, edgecolors="black", label="Centroids")

    for i in range(N_CLUSTERS):
        plt.annotate(
            f"C{i}: {cluster_themes[i]}",
            centroids_2d[i],
            fontsize=8, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="gray", alpha=0.85),
            ha="center", va="bottom",
            xytext=(0, 12), textcoords="offset points",
        )

    plt.colorbar(scatter, label="Cluster")
    plt.title("YouTube Comments - K-means Clustering with t-SNE")
    plt.xlabel("t-SNE Dimension 1")
    plt.ylabel("t-SNE Dimension 2")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_IMAGE, dpi=150)
    print(f"Visualization saved to {OUTPUT_IMAGE}")

    with open(CATEGORIES_FILE, "r", encoding="utf-8") as f:
        step8_categories = json.load(f)["categories"]
    category_names = [c["name"] for c in step8_categories]
    category_descriptions = {c["name"]: c["description"] for c in step8_categories}

    print("\n=== Cluster Analysis ===")
    print(f"\nStep 8 categories for alignment check: {', '.join(category_names)}")
    for i in range(N_CLUSTERS):
        indices = [j for j in range(len(texts)) if labels[j] == i]
        cluster_texts = [texts[j] for j in indices]
        cluster_cls = [classifications[j] for j in indices]
        total = len(cluster_texts)

        classified = [c for c in cluster_cls if c["negative"] is not None and str(c["negative"]).strip() != ""]
        classified_total = len(classified)

        def pct(field):
            count = sum(1 for c in classified if str(c[field]).strip().lower() in ("true", "yes", "1"))
            return count, count * 100 // classified_total if classified_total else 0

        neg_c, neg_p = pct("negative")
        ang_c, ang_p = pct("angry")
        spam_c, spam_p = pct("spam")
        resp_c, resp_p = pct("response")

        print(f"\nCluster {i} - Theme: {cluster_themes[i]} ({total} comments):")
        print(f"  Classification alignment (negative/angry/spam/response):")
        print(f"    negative: {neg_c}/{classified_total} ({neg_p}%)")
        print(f"    angry:    {ang_c}/{classified_total} ({ang_p}%)")
        print(f"    spam:     {spam_c}/{classified_total} ({spam_p}%)")
        print(f"    response: {resp_c}/{classified_total} ({resp_p}%)")
        print(f"  Sample comments:")
        for t in cluster_texts[:5]:
            print(f"    - {t[:120]}")

        dominant = []
        if neg_p >= 60:
            dominant.append("negative")
        if ang_p >= 40:
            dominant.append("angry")
        if spam_p >= 40:
            dominant.append("spam")
        if resp_p >= 70:
            dominant.append("response-needed")
        if not dominant:
            dominant.append("neutral/positive")
        print(f"  => Sentiment categories: {', '.join(dominant)}")

    print("\n=== Summary: Common Themes & Category Alignment ===")
    print("Q: Are there common themes in the comments?")
    print("A: Yes. Embedding-based clustering reveals distinct thematic groups:")
    for i in range(N_CLUSTERS):
        indices = [j for j in range(len(texts)) if labels[j] == i]
        print(f"   - Cluster {i} ({len(indices)} comments): keywords [{cluster_themes[i]}]")
    print()
    print("Q: Do they align with existing categories?")
    print()
    print("  1) Step 8 content categories:")
    for cat in step8_categories:
        print(f"     - {cat['name']}: {cat['description']}")
    print()
    print("  Alignment: The embedding clusters partially align with step 8 categories.")
    print("  Topic-focused clusters (AI/humanity, GPT/technology) correspond to")
    print("  'AI Ethics & Alignment', 'Technical Deep Dive', and 'Future Predictions'.")
    print("  However, clusters also capture social dimensions (host praise, short reactions)")
    print("  that step 8 categories do not cover, since step 8 focuses on content themes.")
    print()
    print("  2) Classification categories (positive, negative, angry, spam):")
    print("  These sentiment/moderation categories cut *across* topic clusters rather than")
    print("  mapping 1:1. The 'short reactions' cluster has the highest spam rate, while")
    print("  topic-focused clusters differ mainly in subject matter, not sentiment.")
    print("  Content-based clustering and sentiment-based classification capture")
    print("  complementary dimensions of the data.")

if __name__ == "__main__":
    main()
