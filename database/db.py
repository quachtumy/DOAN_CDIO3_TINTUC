import pymysql

def get_connection():
    return pymysql.connect(
        host="switchback.proxy.rlwy.net",
        port=12519,
        user="root",
        password="zalXOWZnMSUESimZnuYiqjyGuUakrYsd",
        database="railway",
        charset="utf8mb4",
        connect_timeout=10
    )