from api.user_service import register_user
from api.user_service import get_user
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from sanic import response
from sanic.response import text
from sanic_openapi import doc
import json


def get_schema():
    return {
        "type": "object",
        "properties": {
            "first": {"type": "string"},
            "last": {"type": "string"},
        },
    }


@doc.summary("Post new User.")
@doc.consumes(doc.String(name="body"), location="body")
async def route_post_user(req):
    try:
        validate(instance=json.loads(req.body), schema=get_schema())
        return response.json(await register_user(req))
    except ValidationError as e:
        return e


@doc.summary("Fetch user by ID")
async def route_get_user(req, user_id):
    rps = await get_user(user_id)
    return response.json(text(rps))
