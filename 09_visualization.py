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
    cursor.execute("SELECT text FROM comments")
    rows = cursor.fetchall()
    conn.close()

    texts = [row[0] for row in rows if row[0]]
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

    # Print cluster analysis with theme identification
    print("\n=== Cluster Analysis ===")
    for i in range(N_CLUSTERS):
        cluster_texts = [texts[j] for j in range(len(texts)) if labels[j] == i]
        print(f"\nCluster {i} ({len(cluster_texts)} comments):")
        print(f"  Sample comments:")
        for t in cluster_texts[:5]:
            print(f"    - {t[:120]}")
    print("\nNote: Examine the sample comments above to identify common themes.")
    print("Clusters may align with categories such as positive, negative, angry, or spam.")

if __name__ == "__main__":
    main()
