from fastapi import FastAPI
from database.db import get_connection
from processing.search.search_service import search
from processing.search.related_service import get_related_articles
from processing.trending.service import get_trending_topics

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

@app.get("/search")
def search_api(q: str, top_k: int = 5):
    return search(q, top_k)

@app.get("/related/{article_id}")
def related_api(article_id: int):
    return get_related_articles(article_id)

@app.get("/trending")
def trending_api():
    return get_trending_topics()
