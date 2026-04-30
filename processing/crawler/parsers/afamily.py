import requests
import time
from bs4 import BeautifulSoup

def crawl_afamily(rss_feeds):
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://afamily.vn/'
    }

    valid_news_data = []
    url_existed = set()

    for category, rss_url in rss_feeds.items():
        try:
            response = requests.get(rss_url, timeout=20)
            if response.status_code != 200:
                continue
        except:
            continue

        xml_soup = BeautifulSoup(response.content, 'xml')
        items = xml_soup.find_all('item')

        # Lấy danh sách link
        news_data = []
        for item in items:
            try:
                title = item.title.text.strip()
                url = item.link.text.strip()

                if url in url_existed:
                    continue

                url_existed.add(url)

                news_data.append({
                    'title': title,
                    'url': url
                })
            except:
                continue

        # Crawl từng bài
        for item in news_data:
            url = item['url']

            try:
                time.sleep(0.5)
                response = requests.get(url, headers=headers, timeout=20)
                if response.status_code != 200:
                    continue

                soup = BeautifulSoup(response.content, 'html.parser')

                article_div = soup.find('article')

                if not article_div:
                    continue

                content_block = []
                text_list = []
                text_existed = set()

                for element in article_div.find_all(['h2', 'p', 'figure']):
                    # Text
                    if element.name == 'h2' or element.name == 'p' :
                        if element.find_parent('figcaption'):
                            continue
                        text = element.text.strip()

                        if not text:
                            continue

                        if text in text_existed:
                            continue
                        text_existed.add(text)

                        content_block.append({
                            'type': 'text',
                            'content': text
                        })

                        text_list.append(text)

                    # Image
                    if element.name == 'figure':
                        img = element.find('img')

                        if img:
                            img_url = img.get('data-src') or img.get('src')
                            caption = ""
                            caption_tag = element.find('figcaption')
                            if caption_tag:
                                caption = caption_tag.text.strip()
                            content_block.append({
                                'type': 'image',
                                'url': img_url,
                                'caption': caption
                            })
                texts = '. '.join(text_list)

                # Author
                author = None
                author_tag = soup.find('span', class_='afcba-name')
                if author_tag:
                    author = author_tag.text.strip()
                    author = author[:-1]

                # Published time
                try:
                    published_at = soup.find('span', class_='afcba-time').text.strip()
                except:
                    published_at = None

                # build object
                data = {
                    'title': item['title'],
                    'content': texts,
                    'content_block': content_block,
                    'author': author,
                    'url': url,
                    'published_at': published_at,
                    'source': 'Afamily'
                }

                # lọc bài rỗng
                if len(texts) > 100:
                    valid_news_data.append(data)

            except:
                continue

    return valid_news_data