import psycopg2

def get_user_by_username(connection,username: str):
    # query a user from the database by using their username
    query = "SELECT id,username,hashed_password FROM users WHERE username=%s;"
    try:
        with connection.cursor() as cursor:
            cursor.execute(query,(username,))
            return cursor.fetchone() # returns the id,username,hashed_password or None
    except psycopg2.Error as e:
        print(f"Database error fetching user {e}")
        return None

def create_user(connection,username: str,hashed_password: str):
    # inserts a new user with their username and their unique hashed password
    query = "INSERT INTO users(username,hashed_password) VALUES (%s,%s) RETURNING id,username;"
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query,(username,hashed_password))
                result = cursor.fetchone()
                if result:
                    return{"id":result,"username":result[1]}
                return None

    except psycopg2.Error as e:
        print(f"Database error creating user {e}")
        return None

