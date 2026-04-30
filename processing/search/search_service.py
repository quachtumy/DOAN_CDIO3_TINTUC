import joblib
from processing.search.hybrid_search import hybrid_search
from database.db import get_connection

# load 1 lần
data = joblib.load('models/embeddings.pkl')

ids = data['ids']
texts = data['texts']
embeddings = data['embeddings']


def search(query, top_k=5):
    results = hybrid_search(query, ids, texts, embeddings, top_k)

    # lấy list id
    article_ids = [r['id'] for r in results]

    if not article_ids:
        return []

    conn = get_connection()
    cursor = conn.cursor()

    # query 1 lần 
    format_strings = ','.join(['%s'] * len(article_ids))

    cursor.execute(f"""
        SELECT id, title, content
        FROM Articles
        WHERE id IN ({format_strings})
    """, tuple(article_ids))

    rows = cursor.fetchall()
    conn.close()

    # map id -> data
    data_map = {
        r[0]: {
            'title': r[1],
            'content': r[2]
        }
        for r in rows
    }

    # giữ đúng thứ tự theo search score
    final = []

    for r in results:
        article_id = r['id']

        if article_id in data_map:
            final.append({
                'id': article_id,
                'title': data_map[article_id]['title'],
                'content': data_map[article_id]['content']
            })

    return final