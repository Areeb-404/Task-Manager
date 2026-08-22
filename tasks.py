import json

tasks = [
    {"id" : 1, "Title" : "Buy Groceries", "completed" : True},
    {"id" : 2, "Title" : "Study Python Basics", "completed" : False}
]

def main():
    print("------Task Manager------")
    print(f"Loaded {len(tasks)} tasks into memory.\n")

    for task in tasks:
        status = "[X] " if task["completed"] else "[ ] "
        print(f"{status}{task['id']}: {task['Title']}")

if __name__ == "__main__":
    main()
