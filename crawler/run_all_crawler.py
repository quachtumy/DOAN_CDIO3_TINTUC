from crawler.parsers.vnexpress import crawl_vnexpress
from crawler.parsers.dantri import crawl_dantri
from crawler.parsers.kenh14 import crawl_kenh14
from crawler.parsers.afamily import crawl_afamily
from crawler.parsers.cafebiz import crawl_cafebiz

from crawler.config import vnexpress_rss_feeds, dantri_rss_feeds, kenh14_rss_feeds, afamily_rss_feeds, cafebiz_rss_feeds

from database.db import get_connection
import json

conn = get_connection()
cursor = conn.cursor()

# vnexpress_data = crawl_vnexpress(vnexpress_rss_feeds)
# dantri_data = crawl_dantri(dantri_rss_feeds)
# kenh14_data = crawl_kenh14(kenh14_rss_feeds)
# afamily_data = crawl_afamily(afamily_rss_feeds)
cafebiz_data = crawl_cafebiz(cafebiz_rss_feeds)

# data = [vnexpress_data, dantri_data, kenh14_data, afamily_data, cafebiz_data]

print('Start crawling:')
for item in cafebiz_data:
    cursor.execute('''
        INSERT IGNORE INTO articles
        (title, content, content_block, url, source, published_at)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (
        item['title'],
        item['content'],
        json.dumps(item['content_block'], ensure_ascii=False),
        item['url'],
        item['source'],
        item['published_at']
    ))
print('Done!')
conn.commit()