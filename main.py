from os import stat
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import tasks  #importing the tasks.py file in this file
from database import get_db,create_tables
import security
import users

app = FastAPI(title="Task Manager API")

class UserCreate(BaseModel):
    username:str
    password:str

class TaskCreate(BaseModel):
    title:str
    completed:bool = False # the default value is false

class UserLogin(BaseModel):
    username:str
    password:str

# this below code tells fastapi to read the token from the authorisation header
# the "tokenurl=login" tells swagger where to send the username/password to recieve a token automatically
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
def get_current_user(token:str = Depends(oauth2_scheme),conn=Depends(get_db)):
    # fastapi dependency to extract, verify, and authenticate incoming JWT requests
    # 1. Decoding and verifying the token signature and expiration
    payload = security.decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORISED,
            detail="could not validate credentials",
            headers={"WWW_Authenticate" : "Bearer"},
        )
    # 2. Extracting the user identity claim from the payload (the 'sub' claim holds user ID)
    user_id = payload.get("sub")
    username = payload.get("username")
    if not user_id or not isinstance(username,str):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORISED,
            detail="could not validate credentials",
            headers={"WWW_Authenticate" : "Bearer"},
        )
    # 3. Double checking that the user still exists in the database
    user_record = users.get_user_by_username(conn,username)
    if not user_record:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORISED,
            detail="User Not Found",
            headers={"WWW_Authenticate" : "Bearer"},
        )
    # 4. Return the authenticated user information
    return{"id" : int(user_id), "username" : username}
@app.on_event("startup")
def on_startup():
    create_tables()
@app.get("/")
def read_root():
    return {"message" : "Welcome to your task manager API!"}

@app.get("/tasks")
def get_all_tasks(conn=Depends(get_db), current_user = Depends(get_current_user)): # depends only needs the function definition, not the function call, depends decides when to call the function by itself.
    # calling the database helper function from tasks.py
    return tasks.get_tasks_for_web(conn,current_user["id"])

@app.post("/tasks")
def create_task(task : TaskCreate,conn = Depends(get_db), current_user = Depends(get_current_user)):
    new_task = tasks.add_tasks(conn,task.title,current_user["id"])
    if not new_task:
        raise HTTPException(
            status_code=500,
            detail="Could not create the task."
        )
    return new_task

@app.patch("/tasks/{task_id}")
def toggle_task_status(task_id : int,conn = Depends(get_db),current_user = Depends(get_current_user)):
    updated_task = tasks.toggle_task(conn,task_id,current_user["id"])

    if updated_task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with ID {task_id} not found"
        )
    return updated_task

@app.delete("/tasks/{task_id}")
def delete_task_req(task_id : int,conn=Depends(get_db),current_user = Depends(get_current_user)):
    success = tasks.delete_task(conn,task_id,current_user["id"])
    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"Task with ID {task_id} not found"
        )
    return {
        "message" : f"Task with ID {task_id} successfully deleted"
    }

@app.post("/register",status_code=201)
def register_user(user_data:UserCreate,conn=Depends(get_db)):
    # api route to register a new user using a username with a hashed password
    existing_user = users.get_user_by_username(conn,user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username is already registered."
        )
    # Hash the password given by the user
    hashed_password = security.hash_password(user_data.password)

    # Store the password in the users table
    new_user = users.create_user(conn,user_data.username,hashed_password)
    if not new_user:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while creating your account."
        )
    return new_user

@app.post("/login")
def login_user(form_data : OAuth2PasswordRequestForm = Depends(), conn=Depends(get_db)):
    # authenticate user and return a signed JWT token
    user_record = users.get_user_by_username(conn,form_data.username)
    if not user_record:
        raise HTTPException(
            status_code=401,
            detail="Invalid Username or Password"
        )
    # unpacking the tuple recieved from the database
    db_id,db_username,db_hashed_password = user_record
    # verifying the user's entered password against the bcrypt hash
    if not security.verify_password(form_data.password,db_hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    # creating the jwt token for if the user is verified
    token_data = {"sub":str(db_id),"username":db_username}
    token = security.create_access_token(token_data)

    # return the token which follows the standard OAuth2 formatting
    return{"access_token":token,"token_type":"bearer"}

@app.get("/users/me")
def read_users_me(current_user = Depends(get_current_user)):
    # A protected endpoint that only authenticated users can access
    return current_user
