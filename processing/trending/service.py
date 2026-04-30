from database.db import get_connection

def get_trending_topics():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, size
        FROM TrendingTopics
        ORDER BY size DESC
        LIMIT 5
    """)

    topics = cursor.fetchall()
    results = []

    for t in topics:
        topic_id = t[0]

        cursor.execute("""
            SELECT a.id, a.title
            FROM TrendingArticles ta
            JOIN Articles a ON ta.article_title = a.title
            WHERE ta.topic_id = %s
        """, (topic_id,))

        articles = cursor.fetchall()

        if not articles:
            continue

        main_article = {
            "id": articles[0][0],
            "title": articles[0][1]
        }

        related = [
            {"id": a[0], "title": a[1]}
            for a in articles[1:6]
        ]

        results.append({
            "main_article": main_article,
            "size": t[1],
            "related": related
        })

    conn.close()
    return results