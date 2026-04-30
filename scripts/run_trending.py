from processing.trending.build_trending import (
    load_data,
    group_articles,
    build_topics,
    save_trending
)

def run_build_trending():
    print("Building trending...")

    ids, texts, embeddings = load_data()
    groups = group_articles(texts, embeddings)
    topics = build_topics(groups, ids, texts)

    save_trending(topics)

    print("Trending saved to DB")


if __name__ == "__main__":
    run_build_trending()