import joblib
from sentence_transformers import SentenceTransformer
from database.db import get_connection

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")


def run_embedding():
    conn = get_connection()
    cursor = conn.cursor()

    # lấy bài chưa embedding
    cursor.execute("""
        SELECT id, title
        FROM Articles
        WHERE is_embedding = 0
        AND content IS NOT NULL
    """)

    rows = cursor.fetchall()

    print('Total articles:', len(rows))

    if not rows:
        print('No articles to embed')
        return

    ids = []
    texts = []

    for row in rows:
        article_id = row[0]
        title = row[1] or ""

        text = title

        ids.append(article_id)
        texts.append(text)

    # encode
    print('Encoding...')
    embeddings = model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    try:
        data = joblib.load('models/embeddings.pkl')
        old_ids = data['ids']
        old_texts = data['texts']
        old_embeddings = data['embeddings']
    except:
        old_ids, old_texts, old_embeddings = [], [], []

    # append
    new_ids = old_ids + ids
    new_texts = old_texts + texts
    new_embeddings = list(old_embeddings) + list(embeddings)

    joblib.dump({
        'ids': new_ids,
        'texts': new_texts,
        'embeddings': new_embeddings
    }, 'models/embeddings.pkl')

    # update DB
    for article_id in ids:
        cursor.execute("""
            UPDATE Articles
            SET is_embedding = 1
            WHERE id = %s
        """, (article_id,))

    conn.commit()
    conn.close()

    print(f'Embedded {len(ids)} articles')