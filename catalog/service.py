from catalog.repository import ProductRepository
from core.service import AbstractService


class ProductService(AbstractService):
    """Class representing the product service."""

    _repository = ProductRepository
