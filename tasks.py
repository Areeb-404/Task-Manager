import os
import sqlite3



def add_tasks(conn, title:str):
    query = """
    INSERT INTO tasks (title,completed)
    VALUES(%s,%s)
    RETURNING id, title, completed;
    """

    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(query,(title,False))
                new_row = cursor.fetchone()
        if new_row:
            task_id, title, completed = new_row
            return{
                "id" : task_id,
                "title" : title,
                "completed" : completed
            }

    except Exception as e:
        print(f"Failed to insert task: {e}")


def get_tasks_for_web(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, title, completed FROM tasks")
            rows = cursor.fetchall()
    except Exception as e:
        print(f"Database query failed: {e}")
        return []

    if not rows:
        print("[System] no tasks found in the database! Go ahead and add a task.")
        return []

    task_list = []
    print("------Current Tasks-------")
    for row in rows:
        task_id, title, completed = row
        task_list.append({
            "id" : task_id,
            "title": title,
            "completed": completed}
        )
    return task_list

def toggle_task(conn, task_id:int):
    query = """
    UPDATE tasks
    SET completed = NOT completed  
    WHERE id = %s 
    RETURNING id, title, completed;
    """
    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(query,(task_id,))
                updated_row = cursor.fetchone()
        if updated_row:
            task_id, title, completed = updated_row
            return{
                "id" : task_id,
                "title" : title,
                "completed" : completed
            }
        return None
    except Exception as e:
        print(f"Failed to toggle task: {e}")
        return None

def delete_task(conn,task_id:int):
    query = """
    DELETE FROM tasks WHERE id = %s RETURNING id;
    """
    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(query,(task_id,))
                deleted_row = cursor.fetchone()
        
        return deleted_row is not None
    except Exception as e:
        print(f"Failed to delete task: {e}")
        return False


