import psycopg2
from fastapi import Depends,FastAPI

app = FastAPI(title="Task Manager API")

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


