from database.db import get_connection
from processing.summarization.pipeline import summarize_pipeline


# 🔹 lấy bài chưa summary
def get_unsummarized_articles(limit=50):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, content
        FROM Articles
        WHERE summary IS NULL
        AND content IS NOT NULL
        LIMIT %s
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return rows


# 🔹 update summary
def update_summary(article_id, summary):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE Articles
        SET summary = %s
        WHERE id = %s
    """, (summary, article_id))

    conn.commit()
    conn.close()


# 🔥 MAIN PIPELINE
def run_summary_pipeline(limit=50):
    print("🔹 Start summarizing...")

    while True:
        articles = get_unsummarized_articles(limit)

        if not articles:
            print("✅ Done ALL articles")
            break

        for article_id, content in articles:
            try:
                print(f"Summarizing ID: {article_id}")

                bullets = summarize_pipeline(content)

                if not bullets:
                    continue

                summary_text = "\n".join(bullets)

                update_summary(article_id, summary_text)

            except Exception as e:
                print(f"❌ Error ID {article_id}: {e}")