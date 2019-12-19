from sanic.views import HTTPMethodView
from sanic.response import text
from api.user_service import register_user
from api.user_service import get_user
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from sanic import response
import aiotask_context as context
import json

def get_schema():
    return {
        "type": "object",
        "properties": {
            "first": {"type": "string"},
            "last": {"type": "string"},
        },
    }

async def route_post_user(req):
    try:
        validate(instance=json.loads(req.body), schema=get_schema())
        resp = {"id", text(await register_user(req))}
        return response.json(resp)
    except ValidationError as e:
        return e

async def route_get_user(req,user_id):
    rps = await get_user(user_id)
    return response.json(text(rps))
