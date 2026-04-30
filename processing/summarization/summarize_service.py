import time
from database.db import get_connection
from processing.summarization.pipeline import summarize_pipeline


def run_summary():
    conn = get_connection()
    cursor = conn.cursor()

    total = 0

    while True:
        cursor.execute("""
            SELECT id, content
            FROM Articles
            WHERE summary IS NULL
            AND content IS NOT NULL
            LIMIT 50
        """)

        rows = cursor.fetchall()

        if not rows:
            print('Done ALL articles')
            break

        print(f'Processing batch: {len(rows)}')

        for article_id, content in rows:
            try:
                print(f'Summarizing ID: {article_id}')

                bullets = summarize_pipeline(content)

                summary_text = '\n'.join(bullets)

                cursor.execute("""
                    UPDATE Articles
                    SET summary = %s
                    WHERE id = %s
                """, (summary_text, article_id))

                conn.commit()

                total += 1

                # giảm spam API
                time.sleep(1.2)

            except Exception as e:
                print(f'Error ID {article_id}: {e}')

    conn.close()

    print(f'Total summarized: {total}')