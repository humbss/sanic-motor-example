import json
from util.motor_connection import get_connection
from bson.objectid import ObjectId
from sanic.response import text
from pymongo.errors import ServerSelectionTimeoutError
from sanic.log import logger
from sanic.exceptions import ServerError


async def register_user(user):
    try:
        result = await get_connection().users.insert_one(json.loads(user.body))
        return {"success": "true", "id": text(result.inserted_id)}
    except ServerSelectionTimeoutError as e:
        logger.error("[DB] Error connecting to database: %s",e)
        raise ServerError("Service Error", status_code=500)

async def get_user(id):
    try:
        async for document in get_connection().users.find({"_id": ObjectId(id)}):
            return document
    except ServerSelectionTimeoutError as e:
        logger.error("[DB] Error connecting to database: %s",e)
        raise ServerError("Service Error", status_code=500)

