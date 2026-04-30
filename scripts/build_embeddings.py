from processing.clustering.embedder import encode_texts
from database.db import get_connection
import joblib

def get_all_articles():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, title FROM Articles")
    rows = cursor.fetchall()
    conn.close()

    ids = []
    texts = []

    for row in rows:
        ids.append(row[0])
        texts.append(row[1] or "")

    return ids, texts


if __name__ == "__main__":
    ids, texts = get_all_articles()

    print("🔹 Encoding...")
    embeddings = encode_texts(texts)

    joblib.dump({
        "ids": ids,
        "texts": texts,
        "embeddings": embeddings
    }, "models/embeddings.pkl")

    print("✅ Saved embeddings")