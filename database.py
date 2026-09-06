import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST",os.getenv("DB_HOST_ENV","127.0.0.1"))
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
    # FOR THE USERS TABLE
    create_users_table = """
    CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,
        username VARCHAR(100) UNIQUE NOT NULL,
        hashed_password VARCHAR(255) NOT NULL);
    """

    # FOR THE TASKS TABLE
    create_tasks_table = """
    CREATE TABLE IF NOT EXISTS tasks(
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        completed BOOLEAN DEFAULT FALSE
        );
    """

    # Adding the user_id as a foreign key to tasks table to connect the two
    migrate_tasks_table = """
    ALTER TABLE tasks ADD COLUMN IF NOT EXISTS user_id INT REFERENCES users(id) ON DELETE CASCADE;
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
                cursor.execute(create_users_table)
                cursor.execute(create_tasks_table)
                cursor.execute(migrate_tasks_table)

        print("Database Tables verified/created successfully!")
    finally:
        connection.close()
