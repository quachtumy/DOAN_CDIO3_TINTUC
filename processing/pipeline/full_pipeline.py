from processing.crawler.crawler_service import run_all_crawler
from processing.classification.classification_service import run_classification
from processing.embedding.embedding_service import run_embedding
from processing.trending.trending_service import run_trending

def run_full_pipeline():
    # Này là để khi chạy pipeline này là nó tự động crawl, phân loại, embedding và lấy ra trending lưu vào DB
    print('\nSTART FULL PIPELINE\n')

    run_all_crawler()

    run_classification()

    run_embedding()

    run_trending()

    print('\nDONE FULL PIPELINE\n')