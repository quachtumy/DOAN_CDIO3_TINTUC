CREATE TABLE Articles (
    id INT AUTO_INCREMENT PRIMARY KEY,

    title TEXT,
    content LONGTEXT,
    content_block LONGTEXT,
    url VARCHAR(500) UNIQUE,
    source VARCHAR(100),
    author VARCHAR(100),
    published_at TEXT,
    
    category VARCHAR(100),

    summary LONGTEXT,
    
    data_type ENUM('train', 'prod') DEFAULT 'prod',
    is_embedding BIT DEFAULT 0
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

alter table Articles
add is_embedding bit default 0
update Articles
set is_embedding = 0 where id > 0

alter table Articles
add author varchar(100)
update Articles
set data_type = 'train' where id > 0
select * from Articles order by id desc