import joblib
from sklearn.metrics.pairwise import cosine_similarity
from database.db import get_connection

# load 1 lần
data = joblib.load('models/embeddings.pkl')

ids = data['ids']
texts = data['texts']
embeddings = data['embeddings']

# map id -> index
id_to_index = {id_: i for i, id_ in enumerate(ids)}


def get_related_articles(article_id, top_k=5):
    if article_id not in id_to_index:
        return []

    idx = id_to_index[article_id]

    # lấy embedding của bài hiện tại
    query_emb = embeddings[idx]

    # tính similarity với tất cả
    sims = cosine_similarity([query_emb], embeddings)[0]

    # sort giảm dần
    ranked = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)

    results = []

    for i, score in ranked:
        if ids[i] == article_id:
            continue  # bỏ chính nó

        results.append(ids[i])

        if len(results) >= top_k:
            break

    # lấy dữ liệu từ DB
    conn = get_connection()
    cursor = conn.cursor()

    format_strings = ','.join(['%s'] * len(results))

    cursor.execute(f"""
        SELECT id, title
        FROM Articles
        WHERE id IN ({format_strings})
    """, tuple(results))

    rows = cursor.fetchall()
    conn.close()

    # map id -> title
    data_map = {r[0]: r[1] for r in rows}

    final = []

    for rid in results:
        if rid in data_map:
            final.append({
                'id': rid,
                'title': data_map[rid]
            })

    return final