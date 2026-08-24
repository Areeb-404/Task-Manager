import json

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

tasks = [
    {"id" : 1, "Title" : "Buy Groceries", "completed" : True},
    {"id" : 2, "Title" : "Study Python Basics", "completed" : False}
]

def main():
    print("------Task Manager------")
    print(f"Loaded {len(tasks)} tasks into memory.\n")
    add_tasks("Finish Mass Effect 3")
    toggle_task(3)
    get_tasks()
    delete_task(5)
    get_tasks()

if __name__ == "__main__":
    main()
