from abc import ABC
from bson.objectid import ObjectId


class AbstractService(ABC):
    """Class representing the abstract base service."""

    _repository = None

    @classmethod
    async def get(cls, filters={}, options={}):
        """Retrieve all data by filters."""
        return await cls.get_repository().get(filters, options)

    @classmethod
    async def find(cls, filters):
        """Find data by filters."""
        filters = {'_id': ObjectId(filters['_id'])}
        return await cls.get_repository().find(filters)

    @classmethod
    async def create(cls, payload):
        """Save a new register."""
        return await cls.get_repository().create(payload)

    @classmethod
    async def update(cls, filters, payload):
        """Update data by filters."""
        filters = {'_id': ObjectId(filters['_id'])}
        payload = {'$set': payload}
        return await cls.get_repository().update(filters, payload)

    @classmethod
    async def delete(cls, filters):
        """Delete data by filters."""
        filters = {'_id': ObjectId(filters['_id'])}
        return await cls.get_repository().delete(filters)

    @classmethod
    def get_repository(cls):
        """Get repository."""
        if cls._repository is None:
            raise ValueError('Repository is required, set _repository')
        return cls._repository
