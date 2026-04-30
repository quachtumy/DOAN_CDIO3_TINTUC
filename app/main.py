from fastapi import FastAPI
from database.db import get_connection
from processing.search.search_service import search
from processing.search.related_service import get_related_articles

app = FastAPI()

# Lấy ra 20 bài báo (random)
@app.get('/articles')
def get_all_articles():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT a.id, a.title, a.content, a.content_block
        FROM Articles a
        JOIN (
            SELECT id
            FROM Articles
            WHERE title IS NOT NULL and summary IS NOT NULL
            ORDER BY RAND(0)
            LIMIT 20
        ) AS t ON a.id = t.id;
    """)

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            'id': row[0],
            'title': row[1],
            'content': row[2][:200],
            'content_block': row[3]
        }
        for row in rows
    ]

# Lấy ra thông tin chi tiết bài báo
@app.get('/articles/{articles_id}')
def get_one_articles(articles_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, content, source, published_at, category, summary
        FROM Articles
        WHERE id = %s
    """, (articles_id))

    row = cursor.fetchone()
    conn.close()

    return {
        'id': row[0],
        'title': row[1],
        'content': row[2],
        'source': row[3],
        'published_at': row[4],
        'category': row[5],
        'summary': row[6]
    }

# Lấy ra các bài báo liên quan khi người dùng nhập từ khoá
@app.get('/search')
def search_api(q: str, top_k: int = 5):
    return search(q, top_k)

# Lấy ra các bài báo liên quan khi người dùng nhấp vào xem một bài nào đó
@app.get('/related/{article_id}')
def related_api(article_id: int):
    return get_related_articles(article_id)

# Lấy ra danh sách bài báo nổi bật
@app.get('/trending')
def get_trending():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, main_article, size
        FROM TrendingTopics
        ORDER BY size DESC
    """)

    topics = cursor.fetchall()

    result = []

    for t in topics:
        topic_id = t[0]

        cursor.execute("""
            SELECT A.id, A.title
            FROM TrendingArticles TA
            JOIN Articles A ON TA.article_id = A.id
            WHERE TA.topic_id = %s
            LIMIT 5
        """, (topic_id,))

        articles = cursor.fetchall()

        result.append({
            'title': t[1],
            'size': t[2],
            'articles': [
                {'id': a[0], 'title': a[1]} for a in articles
            ]
        })

    conn.close()

    return result