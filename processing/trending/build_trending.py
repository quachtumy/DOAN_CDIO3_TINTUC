from database.db import get_connection

def save_trending(topics):
    conn = get_connection()
    cursor = conn.cursor()

    # xoá data cũ
    cursor.execute("DELETE FROM TrendingArticles")
    cursor.execute("DELETE FROM TrendingTopics")

    for t in topics:
        main_id = t["main_article"]["id"]
        size = t["size"]

        # insert topic
        cursor.execute("""
            INSERT INTO TrendingTopics (main_article_id, size)
            VALUES (%s, %s)
        """, (main_id, size))

        topic_id = cursor.lastrowid

        # insert related articles
        for r in t["related"]:
            cursor.execute("""
                INSERT INTO TrendingArticles (topic_id, article_id)
                VALUES (%s, %s)
            """, (topic_id, r["id"]))

    conn.commit()
    conn.close()
    