from catalog.model import ProductModel
from core.repository import AbstractRepository


class ProductRepository(AbstractRepository):
    """Class representing the product repository."""

    _model = ProductModel
