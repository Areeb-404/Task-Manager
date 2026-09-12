import os

import psycopg2



def add_tasks(conn, title:str, user_id:int):
    query = """
    INSERT INTO tasks (title,completed,user_id)
    VALUES(%s,%s,%s)
    RETURNING id, title, completed, user_id;
    """

    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(query,(title,False,user_id))
                new_row = cursor.fetchone()
        if new_row:
            task_id, title, completed, u_id = new_row
            return{
                "task id" : task_id,
                "title" : title,
                "completed" : completed,
                "user id" : u_id
            }

    except Exception as e:
        print(f"Failed to insert task: {e}")


def get_tasks_for_web(conn,user_id : int):
    query = "SELECT id, title, completed FROM tasks WHERE user_id = %s ORDER BY id;"
    try:
        with conn.cursor() as cursor:
            cursor.execute(query,(user_id,))
            rows = cursor.fetchall()
    except psycopg2.Error as e:
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
            "task id" : task_id,
            "title": title,
            "completed": completed}
        )
    return task_list

def toggle_task(conn, task_id:int, user_id:int):
    query = """
    UPDATE tasks
    SET completed = NOT completed  
    WHERE id = %s AND user_id = %s 
    RETURNING id, title, completed, user_id;
    """
    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(query,(task_id,user_id))
                updated_row = cursor.fetchone()
        if updated_row:
            task_id, title, completed, u_id = updated_row
            return{
                "task_id" : task_id,
                "title" : title,
                "completed" : completed,
                "user_id" : u_id
            }
        return None
    except Exception as e:
        print(f"Failed to toggle task: {e}")
        return None

def delete_task(conn,task_id:int, user_id:int):
    query = """
    DELETE FROM tasks WHERE id = %s AND user_id = %s RETURNING id;
    """
    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(query,(task_id,user_id))
                deleted_row = cursor.fetchone()
                return deleted_row is not None
    except Exception as e:
        print(f"Failed to delete task: {e}")
        return False


