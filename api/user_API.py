from service.user_service import register_user, get_user
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from sanic.response import text
from sanic_openapi import doc
from util.generic_except import get_response_error
from sanic.exceptions import ServerError
from sanic import response
import json


def get_schema():
    return {
        "type": "object",
        "properties": {"first": {"type": "string"}, "last": {"type": "string"},},
    }


@doc.summary("Post new User.")
@doc.consumes(doc.String(name="body"), location="body")
async def route_post_user(req):
    try:
        validate(instance=json.loads(req.body), schema=get_schema())
        return response.json(await register_user(req))
    except ValidationError as ve:
        return get_response_error("user.validation.error",ve.args)
    except ServerError as se:
        return get_response_error("user.post.generic.error",se)

@doc.summary("Fetch user by ID")
async def route_get_user(req, user_id):
    try:
        user = await get_user(user_id)
        return response.json(text(user))
    except ServerError as se:
        return get_response_error("user.get.generic.error",se)