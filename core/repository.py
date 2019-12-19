from abc import ABC
from db.motor_connection import get_connection
from pymongo import ReturnDocument
import aiotask_context as context
import urllib.parse
import math


class AbstractRepository(ABC):
    """Class representing the abstract base repository."""

    _model = None

    @classmethod
    async def get(cls, filters={}, options={}):
        """Retrieve all data by filters."""

        cls._limit = cls._get_limit(options)
        cls._page = cls._get_page(options)
        cls._count = await cls.count(filters)
        cls._page_count = int(math.ceil(cls._count / cls._limit))

        collection = cls.get_model().get_collection_name()
        data = await get_connection()[collection].find(filters).skip(cls._limit * (cls._page - 1)).to_list(cls._limit)

        response = {
          'data': cls._serialize(data),
          'links': {
              'first': cls._get_url(1),
              'last': cls._get_url(cls._page_count),
              'prev': (
                  cls._get_url(cls._page - 1)
                  if cls._validate_page(cls._page - 1) else None
              ),
              'next': (
                  cls._get_url(cls._page + 1)
                  if cls._validate_page(cls._page + 1) else None
              )
          },
          'meta': {
              'current_page': cls._page,
              'last_page': cls._page_count,
              'per_page': cls._limit,
              'total': cls._count,
          }
        }

        return response

    @classmethod
    def _validate_page(cls, page):
        if cls._count > 0:
            if page > cls._page_count or page < 1:
                return None

            return page

        return False

    @classmethod
    def _get_url(cls, page):
        """"Get current URL with page query string."""
        request = context.get('request')
        url_parts = list(urllib.parse.urlparse(request.url))
        query = dict(urllib.parse.parse_qsl(url_parts[4]))
        query.update({'page': page})
        url_parts[4] = urllib.parse.urlencode(query)

        return urllib.parse.urlunparse(url_parts)

    @classmethod
    async def count(cls, filters={}):
        """Count the number of documents in this collection."""

        collection = cls.get_model().get_collection_name()
        data = await get_connection()[collection].count_documents(filters)

        return data

    @classmethod
    async def find(cls, filters):
        """Find data by filters."""
        collection = cls.get_model().get_collection_name()
        doc = await get_connection()[collection].find_one(filters)

        return cls._serialize(doc)

    @classmethod
    async def create(cls, payload):
        """Save a new register."""
        collection = cls.get_model().get_collection_name()
        doc = await get_connection()[collection].insert_one(payload)
        return await cls.find({'_id': doc.inserted_id})

    @classmethod
    async def update(cls, filters, payload):
        """Update data by filters."""
        collection = cls.get_model().get_collection_name()
        doc = await get_connection()[collection].find_one_and_update(
          filters, payload, return_document=ReturnDocument.AFTER
        )
        return cls._serialize(doc)

    @classmethod
    async def delete(cls, payload):
        """Delete data by filters."""
        collection = cls.get_model().get_collection_name()
        doc = await get_connection()[collection].delete_one(payload)
        return doc

    @classmethod
    def get_model(cls):
        """Get the model."""
        if cls._model is None:
            raise ValueError('Model is required, set _model')
        return cls._model

    @classmethod
    def _get_page(cls, options):
        """Get current page."""
        page = int(options.get('page', 1))
        return page if page > 0 else 1

    @classmethod
    def _get_limit(cls, options):
        """Get limit of registers."""
        limit = int(options.get('limit', cls.get_model().get_limit()))
        return limit if limit <= cls.get_model().get_max_limit() else cls.get_model().get_max_limit()

    @classmethod
    def _serialize(cls, data):
        """Serialize data."""

        if data:
            if isinstance(data, dict):
                data['id'] = str(data['_id'])
                del data['_id']
            elif isinstance(data, list):
                for doc in data:
                    doc['id'] = str(doc['_id'])
                    del doc['_id']
        return data
