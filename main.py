import os
from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr
from pymongo import MongoClient
from dotenv import load_dotenv
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response, JSONResponse
from bson import ObjectId, json_util
import json
from typing import Optional, List

load_dotenv()  # take environment variables from .env.

mongodb_url = os.environ.get("MONGODB_URL")

client = MongoClient(mongodb_url)

app = FastAPI()

# app.add_event_handler("startup", client)
# app.add_event_handler("shutdown", client)
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    name: str
    username: str
    email: str

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def parse_json(data):
    return json.loads(json_util.dumps(data))

@app.get("/", response_model=List[UserResponse], tags=["User"])
async def get_users():
    res = client.fastAPI.users.find()
    return parse_json(res)

@app.get("/users/{username}", response_model=UserResponse, tags=["User"])
async def get_user(username: str):
    res = client.fastAPI.users.find_one({"username": username})
    return res

@app.post("/", tags=["User"])
async def add_user(user: User):
    print('Name: {2} \nMobile: {1},\nEmail: {0}'.format(user.email, user.username, user.name))
    client.fastAPI.users.insert_one(jsonable_encoder(user))
    return { "message" : 'success' }
