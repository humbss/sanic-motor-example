from sanic import Sanic
from api.user_API import route_post_user
from api.user_API import route_get_user

def add_routes(app):
    app.add_route(route_post_user, '/user', methods=['POST'])
    app.add_route(route_get_user, '/user/<user_id>', methods=['GET'])