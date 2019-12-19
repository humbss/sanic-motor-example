from sanic import Sanic
from sanic.response import json
from api.user_API import route_post_user
from api.user_API import route_get_user
from catalog.view import ProductListView, ProductDetailView

def add_routes(app):
    app.add_route(route_post_user, '/user', methods=['POST'])
    app.add_route(route_get_user, '/user/<user_id>', methods=['GET'])
    app.add_route(ProductListView.as_view(), '/catalog/products')
    app.add_route(ProductDetailView.as_view(), '/catalog/products/<id>')
