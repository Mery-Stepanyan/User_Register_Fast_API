from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

users = {}

class User(BaseModel):
    username: str
    password: str


@app.post("register")
def register(user: User):
    if user.username in users:
        raise HTTPException(status_code=400, detail="User already registered")
    users[user.username] = user.password
    return {"message": "User registered successfully"}


@app.post("login")
def login(user: User):
    if user.username not in users or users[user.username] != user.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful"}



