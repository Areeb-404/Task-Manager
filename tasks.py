import json

def get_tasks():
    if not tasks:
        print("\nYour task list is empty!")
    for task in tasks:
        status = "[X] " if task["completed"] else "[ ] "
        print(f"{status}{task['id']}: {task['Title']}")

tasks = [
    {"id" : 1, "Title" : "Buy Groceries", "completed" : True},
    {"id" : 2, "Title" : "Study Python Basics", "completed" : False}
]

def main():
    print("------Task Manager------")
    print(f"Loaded {len(tasks)} tasks into memory.\n")
    get_tasks()

if __name__ == "__main__":
    main()
