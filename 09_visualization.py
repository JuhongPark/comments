import sqlite3
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from sentence_transformers import SentenceTransformer

DB_FILE = "comments.db"
N_CLUSTERS = 5
OUTPUT_IMAGE = "clusters.png"

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

    # Project centroids to 2D by averaging points per cluster
    centroids_2d = np.array([reduced[labels == i].mean(axis=0) for i in range(N_CLUSTERS)])

    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(reduced[:, 0], reduced[:, 1], c=labels, cmap="tab10", alpha=0.6, s=10)
    plt.scatter(centroids_2d[:, 0], centroids_2d[:, 1], c="red", marker="X", s=200, edgecolors="black", label="Centroids")
    plt.colorbar(scatter, label="Cluster")
    plt.title("YouTube Comments - K-means Clustering with t-SNE")
    plt.xlabel("t-SNE Dimension 1")
    plt.ylabel("t-SNE Dimension 2")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_IMAGE, dpi=150)
    print(f"Visualization saved to {OUTPUT_IMAGE}")

    # Analyze clusters: themes and alignment with classification categories
    print("\n=== Cluster Analysis ===")
    for i in range(N_CLUSTERS):
        indices = [j for j in range(len(texts)) if labels[j] == i]
        cluster_texts = [texts[j] for j in indices]
        cluster_cls = [classifications[j] for j in indices]
        total = len(cluster_texts)

        def pct(field):
            count = sum(1 for c in cluster_cls if str(c[field]).strip().lower() in ("true", "yes", "1"))
            return count, count * 100 // total if total else 0

        neg_c, neg_p = pct("negative")
        ang_c, ang_p = pct("angry")
        spam_c, spam_p = pct("spam")
        resp_c, resp_p = pct("response")

        print(f"\nCluster {i} ({total} comments):")
        print(f"  Classification breakdown:")
        print(f"    negative: {neg_c}/{total} ({neg_p}%)")
        print(f"    angry:    {ang_c}/{total} ({ang_p}%)")
        print(f"    spam:     {spam_c}/{total} ({spam_p}%)")
        print(f"    response: {resp_c}/{total} ({resp_p}%)")
        print(f"  Sample comments:")
        for t in cluster_texts[:5]:
            print(f"    - {t[:120]}")

if __name__ == "__main__":
    main()
