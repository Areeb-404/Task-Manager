import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST","127.0.0.1")
DB_PORT = os.getenv("DB_PORT","5432")
DB_USER = os.getenv("DB_USER","postgres")
DB_NAME = os.getenv("DB_NAME","postgres")

if not DB_PASSWORD:
    raise ValueError("SYSTEM ERROR: 'DB_PASSWORD' IS NOT SET IN YOUR .ENV FILE!")

def get_db():
    connection = psycopg2.connect(
        host = DB_HOST,
        database = DB_NAME,
        user = DB_USER,
        password = DB_PASSWORD,
        port = DB_PORT
    )
    try:
        # handing the connection to fastapi route for dependency use
        yield connection
    finally:
        # to always close the connection after use
        connection.close()

def create_tables():
    query = """
    CREATE TABLE IF NOT EXISTS tasks(
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        completed BOOLEAN DEFAULT FALSE
        );
    """
    connection = psycopg2.connect(
        host = DB_HOST,
        database = DB_NAME,
        user = DB_USER,
        password = DB_PASSWORD,
        port = DB_PORT
    )
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
        print("Database Tables verified/created successfully!")
    finally:
        connection.close()
