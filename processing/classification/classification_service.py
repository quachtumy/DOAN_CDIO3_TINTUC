from database.db import get_connection
from processing.classification.model import NewsClassifier

classifier = NewsClassifier()

def run_classification():
    conn = get_connection()
    cursor = conn.cursor()

    # lấy toàn bộ bài chưa có category
    cursor.execute("""
        SELECT id, content
        FROM Articles
        WHERE category IS NULL
        AND content IS NOT NULL
    """)

    rows = cursor.fetchall()

    print('Total articles:', len(rows))

    for article_id, content in rows:
        try:
            category = classifier.predict(content)

            cursor.execute("""
                UPDATE Articles
                SET category = %s
                WHERE id = %s
            """, (category, article_id))

        except Exception as e:
            print(f'Error ID {article_id}: {e}')

    conn.commit()
    conn.close()
