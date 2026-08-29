import os
import sqlite3


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR,"tasks.db")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        );
                       """)
        conn.commit()
        print("[System] Database initalized Successfully!")

def add_tasks(title,completed):
    completed_int = 1 if completed else 0
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
    # NOTE :The data parameter MUST be a tuple. (title,) is single element tuple the comma is necessary to define as a tuple
    cursor.execute("INSERT INTO tasks (title,completed) VALUES (?,?);",(title,completed_int))
    conn.commit()
    new_id = cursor.lastrowid
    # commit the changes permanently into the disk
    return get_task_by_id(new_id)

def get_tasks_for_web():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id,title,completed FROM tasks")
        rows = cursor.fetchall() # returns all the rows of the query as a list of tuples.

    #If the database is empty i.e. no rows are present in the database
    if not rows:
        print("\n[System] no tasks found in the database! Go ahead and add something.")
        return

    # convert the tasks list into a web-friendly dictionary with key labels for fastAPI
    task_list = []

    print("\n----------Current Tasks------------")
    for row in rows:
        # Unpacking the database tuple returned from the fetchall function using sequence Unpacking
        task_id,title,completed_int = row
        # convert the sqlite3 0/1 integer into a boolean true false value for python
        completed = True if completed_int == 1 else False

        task_list.append({
            "id" : task_id,
            "title" : title,
            "completed" : completed
        })
    return task_list

def get_task_by_id(task_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id,title,completed FROM tasks WHERE id = ?",(task_id,))
        row = cursor.fetchone() # fetches a single tuple or none
    if not row:  # if no such row is found
        return None

    # unpack the tuple into web-friendly dictionary
    db_id,title,completed_int = row
    completed = True if completed_int == 1 else False

    return{
        "id" : task_id,
        "title" : title,
        "completed" : completed
    }

def toggle_task(task_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET completed = 1 - completed WHERE id = ?;",(task_id,)) # '?' acts as a placeholder for the input from the python program which will go there
        # why not use a f string? - the user may input a whole sql command in the id variable which sabotages the program and is also known as an sql injection attack
        # '1 - completed' is a mathematical trick to invert the 1 to a 0 and a 0 to a 1
        conn.commit()

def delete_task(task_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id=?;",(task_id,))

        # check if the task_id row actually exists in the database
        if cursor.rowcount == 0:
            print(f"[System] Error: Task with ID {task_id} not found in the database")
        else:
            conn.commit()
            print(f"\n[System] Task ID {task_id} was Successfully deleted")


