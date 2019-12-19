from sanic.views import HTTPMethodView
from sanic.response import json
from sanic.exceptions import abort
from catalog.service import ProductService


class ProductListView(HTTPMethodView):
    """Class representing the list and create of the product."""

    async def get(self, request):
        data = await ProductService().get(options=request.args)
        return json(data)

    async def post(self, request):
        data = await ProductService().create(request.json)
        return json(data)


class ProductDetailView(HTTPMethodView):
    """Class representing the retrieve, update and delete an product."""

    async def get(self, request, id):
        filters = {'_id': id}
        data = await ProductService().find(filters)

        if not data:
            abort(404)

        return json(data)

    async def put(self, request, id):
        filters = {'_id': id}

        exists = await ProductService().find(filters)
        if not exists:
            abort(404)

        data = await ProductService().update(filters, request.json)
        return json(data)

    async def delete(self, request, id):
        filters = {'_id': id}

        exists = await ProductService().find(filters)
        if not exists:
            abort(404)

        data = await ProductService().delete(filters)
        return json(data)
