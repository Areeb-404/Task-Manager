import psycopg2

def get_db():
    connection = psycopg2.connect(
        host = "127.0.0.1",
        database = "postgres",
        user = "postgres",
        password = "Areeb_2007",
        port = "5432"
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
        completed BOOLEAN DEFAULT TASKS,
        );
    """
    connection = psycopg2.connect(
        host = "127.0.0.1",
        database = "postgres",
        user = "postgres",
        password = "Areeb_2007",
        port = "5432")

    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
        print("Database Tables verified/created successfully!")
    finally:
        connection.close()
