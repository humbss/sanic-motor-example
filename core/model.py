from abc import ABC


class ModelAbstract(ABC):
    """Class representing the abstract base model."""

    _collection = None
    _limit = 25
    _max_limit = 100

    @classmethod
    def get_collection_name(cls):
        """Get collection name."""
        if cls._collection is None:
            raise ValueError('Collection name is required, set _collection')
        return cls._collection

    @classmethod
    def get_limit(cls):
        """Get register limit."""
        return cls._limit

    @classmethod
    def get_max_limit(cls):
        """Get max register limit."""
        return cls._max_limit
