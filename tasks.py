import json
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
    if tasks:
        new_id = tasks[-1]['id']+1
    else:
        new_id = 1

    new_task = {
        "id":new_id,
        "Title" : title,
        "completed": False
    }
    tasks.append(new_task)
    print(f"Added task: '{title}' with id {new_id}")

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
    if not tasks:
        print("\nyour task list is empty!")
    for task in tasks:
        status = "[x] " if task["completed"] else "[ ] "
        print(f"{status}{task['id']}: {task['Title']}")


def toggle_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            status_text = "completed" if task["completed"] else "pending"
            print(f"Task {task['Title']} is now marked as {status_text}")
            return
    print(f"Error! task with id {task_id} was not found.")

def delete_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            print(f"Successfully removed task '{task['Title']}' (ID: {task_id})")
            return
    print(f"Error! task with ID {task_id} was not found")

def save_tasks():
    with open("tasks.json","w",encoding="utf-8") as f:
        json.dump(tasks,f,indent=4)
        print("\n [System] Tasks Successfully saved to tasks.json!")

 
tasks = [
    {"id" : 1, "Title" : "Buy Groceries", "completed" : True},
    {"id" : 2, "Title" : "Study Python Basics", "completed" : False}
]

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
        
        choice = int(input("\nEnter Your Choice(1-5): "))
        
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
            save_tasks()
            print("\nGoodbye! Thanks for using task manager")
            break
        else:
            print("Invalid Choice, Please select a number from 1 to 5.")


if __name__ == "__main__":
    main()
