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

def add_tasks(title):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
    # NOTE :The data parameter MUST be a tuple. (title,) is single element tuple the comma is necessary to define as a tuple
    cursor.execute("INSERT INTO tasks (title) VALUES (?);",(title,))
    # commit the changes permanently into the disk
    conn.commit()
    print(f"\n[System] Task '{title}' added to the database Successfully")


def load_tasks():
    global tasks  # tells python to operate on the global tasks list instead of creating a local variable named tasks
    try:
        with open("tasks.json","r") as f:
            tasks = json.load(f)
            print("[System] Tasks loaded Successfully")
    except FileNotFoundError:
        # if the file does not exist
        print("[System] No save file found. Starting with default tasks.json")
    except json.JSONDecodeError:
        # if the file is not json compliant, i.e. it contains typos or hidden whitespaces
        print("[System] Warning! Save file is corrupted. Starting Empty")

def get_tasks():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id,title,completed FROM tasks")
        rows = cursor.fetchall() # returns all the rows of the query as a list of tuples.

    #If the database is empty i.e. no rows are present in the database
    if not rows:
        print("\n[System] no tasks found in the database! Go ahead and add something.")
        return

    # Print the tasks to the terminal
    print("\n----------Current Tasks------------")
    for row in rows:
        # Unpacking the database tuple returned from the fetchall function using sequence Unpacking
        task_id,title,completed_int = row
        # convert the sqlite3 0/1 integer into a boolean true false value for python
        completed = True if completed_int == 1 else False
        # Display each task with a checkmark accordingly
        status = "✓" if completed else " "
        print(f"[{status}] ID {task_id}: {title}")


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


def main():
    #set up our relational database at startup.
    init_db()
    while True:
        print("\n-----------Task Manager Menu-----------")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Toggle Task Status")
        print("4. Delete Task")
        print("5. Exit")
        
        try:
            choice = int(input("\nEnter Your Choice(1-5): "))
        except ValueError:
            choice = None
        
        if choice==1:
            get_tasks()
        elif choice==2:
            title = input("Enter the title of the new task: ")
            add_tasks(title)
        elif choice==3:
            try:
                task_id = int(input("Enter the task ID: "))
                toggle_task(task_id)
            except ValueError:
                # if input is not a number
                print("Error: Please enter a valid number as ID")
        elif choice==4:
            try:
                task_id = int(input("Enter the task ID: "))
                delete_task(task_id)
            except ValueError:
                # if input is not a number
                print("Error: Please enter a valid number as ID")
        elif choice==5:
            print("\nGoodbye! Thanks for using task manager")
            break
        else:
            print("Invalid Choice, Please select a number from 1 to 5.")


if __name__ == "__main__":
    main()
