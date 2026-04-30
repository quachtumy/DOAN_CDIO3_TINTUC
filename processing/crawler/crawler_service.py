from database.db import get_connection
import json

from processing.crawler.parsers.afamily import crawl_afamily
from processing.crawler.parsers.cafebiz import crawl_cafebiz
from processing.crawler.parsers.dantri import crawl_dantri
from processing.crawler.parsers.kenh14 import crawl_kenh14
from processing.crawler.parsers.vnexpress import crawl_vnexpress


RSS_FEEDS = {
    'vnexpress': {
        'Trang chủ': 'https://vnexpress.net/rss/tin-moi-nhat.rss'
    },
    'dantri': {
        'Trang chủ': 'https://dantri.com.vn/rss/home.rss'
    },
    'kenh14': {
        'Trang chủ': 'https://kenh14.vn/rss/home.rss'
    },
    'afamily': {
        'Trang chủ': 'https://afamily.vn/trang-chu.rss'
    },
    'cafebiz': {
        'Trang chủ': 'https://cafebiz.vn/rss/home.rss'
    }
}

def remove_duplicates():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE a1
        FROM Articles a1
        JOIN Articles a2
        ON a1.url = a2.url
        AND a1.id < a2.id;
    """)

    conn.commit()
    conn.close()

def run_all_crawler():
    conn = get_connection()
    cursor = conn.cursor()

    print("Start crawling...")

    # crawl từng nguồn
    vn_data = crawl_vnexpress(RSS_FEEDS['vnexpress'])
    dantri_data = crawl_dantri(RSS_FEEDS['dantri'])
    kenh14_data = crawl_kenh14(RSS_FEEDS['kenh14'])
    afamily_data = crawl_afamily(RSS_FEEDS['afamily'])
    cafebiz_data = crawl_cafebiz(RSS_FEEDS['cafebiz'])

    print('VNExpress:', len(vn_data))
    print('Dantri:', len(dantri_data))
    print('Kenh14:', len(kenh14_data))
    print('Afamily:', len(afamily_data))
    print('Cafebiz:', len(cafebiz_data))

    # gộp data
    all_articles = vn_data + dantri_data + kenh14_data + afamily_data + cafebiz_data

    print('Total crawled:', len(all_articles))

    inserted = 0

    # insert vào DB
    for item in all_articles:
        try:
            cursor.execute('''
                INSERT IGNORE INTO Articles
                (title, content, content_block, url, source, author, published_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (
                item['title'],
                item['content'],
                json.dumps(item['content_block'], ensure_ascii=False),
                item['url'],
                item['source'],
                item.get('author'),
                item.get('published_at')
            ))

            inserted += cursor.rowcount

        except Exception as e:
            print('Insert error:', e)

    conn.commit()

    remove_duplicates()

    conn.close()

    print(f'Inserted {inserted} new articles')
    print('Done crawling')