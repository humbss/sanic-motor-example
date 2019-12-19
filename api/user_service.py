import json
from db.motor_connection import get_connection
from bson.objectid import ObjectId

async def register_user(user):
    result = await get_connection().users.insert_one(json.loads(user.body))
    return result.inserted_id

async def get_user(id):
    async for document in get_connection().users.find({"_id":ObjectId(id)}):
        return document
    return {}

