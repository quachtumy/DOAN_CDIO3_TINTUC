CREATE TABLE Articles (
    id INT AUTO_INCREMENT PRIMARY KEY,

    title TEXT,
    content LONGTEXT,
    content_block LONGTEXT,
    url VARCHAR(500) UNIQUE,
    source VARCHAR(100),
    published_at TEXT,

    status VARCHAR(20) DEFAULT 'raw',

    category VARCHAR(100),

    summary LONGTEXT
);

CREATE TABLE TrendingTopics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    main_article TEXT,
    size INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE TrendingArticles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    topic_id INT,
    article_title TEXT,
    FOREIGN KEY (topic_id) REFERENCES TrendingTopics(id)
);
select * from Articles where source = N'CafeBiz'