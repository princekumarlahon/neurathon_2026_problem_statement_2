import mysql.connector

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="user",
        password="root",
        database="biz_agent"
    )
