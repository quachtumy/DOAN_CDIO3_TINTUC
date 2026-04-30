import joblib
from sklearn.metrics.pairwise import cosine_similarity
from database.db import get_connection

def group_articles(embeddings, threshold=0.6):
    sim = cosine_similarity(embeddings)

    n = len(embeddings)
    visited = [False] * n
    groups = []

    for i in range(n):
        if visited[i]:
            continue

        group = [i]
        visited[i] = True

        for j in range(i + 1, n):
            if sim[i][j] > threshold:
                group.append(j)
                visited[j] = True

        groups.append(group)

    return groups

def run_trending():
    data = joblib.load('models/embeddings.pkl')

    ids = data['ids']
    texts = data['texts']
    embeddings = data['embeddings']

    print('Total articles:', len(ids))

    groups = group_articles(embeddings)

    print('Total groups:', len(groups))

    topics = []

    for g in groups:
        if len(g) < 3:
            continue

        topics.append({
            'title': texts[g[0]],
            'size': len(g),
            'articles': [ids[i] for i in g]
        })

    topics.sort(key=lambda x: x['size'], reverse=True)
    topics = topics[:5]

    print('Topics kept:', len(topics))

    conn = get_connection()
    cursor = conn.cursor()

    # xoá đúng thứ tự (tránh lỗi FK)
    cursor.execute('DELETE FROM TrendingArticles')
    cursor.execute('DELETE FROM TrendingTopics')

    for t in topics:
        # lưu topic
        cursor.execute("""
            INSERT INTO TrendingTopics (main_article, size)
            VALUES (%s, %s)
        """, (t['title'], t['size']))

        topic_id = cursor.lastrowid

        # lưu articles (chỉ lưu id)
        for article_id in t['articles']:
            cursor.execute("""
                INSERT INTO TrendingArticles (topic_id, article_id)
                VALUES (%s, %s)
            """, (topic_id, article_id))

    conn.commit()
    conn.close()

    print('Trending updated')