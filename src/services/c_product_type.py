from models.cryptography import ProductType

from services.base import BaseRepository


class CryptographyProductTypeServise(BaseRepository):
    model = ProductType
