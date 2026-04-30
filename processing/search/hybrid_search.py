from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# 🔥 load model 1 lần (global)
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# 🔹 keyword score
def keyword_score(query, text):
    query = query.lower()
    text = text.lower()

    words = query.split()

    score = 0

    for w in words:
        if w in text:
            score += 1

    if query in text:
        score += 2

    return score


# 🔹 semantic score
def semantic_scores(query, embeddings):
    query_emb = model.encode([query])
    scores = cosine_similarity(query_emb, embeddings)[0]
    return scores


# 🔥 MAIN FUNCTION (dùng cho API)
def hybrid_search(query, ids, texts, embeddings, top_k=5):
    sem_scores = semantic_scores(query, embeddings)

    results = []

    for i, text in enumerate(texts):
        kw_score = keyword_score(query, text)

        final_score = 0.7 * sem_scores[i] + 0.3 * kw_score

        results.append((i, final_score))

    results.sort(key=lambda x: x[1], reverse=True)

    top_results = []

    for idx, _ in results[:top_k]:
        top_results.append({ "id": ids[idx] })

    return top_results