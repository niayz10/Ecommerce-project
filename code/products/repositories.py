from typing import Protocol
from . import models
from django.db.models import Q, Min, QuerySet


class ProductRepositoriesInterface(Protocol):

    @staticmethod
    def get_products() -> QuerySet[models.Product]:
        ...

class ProductRepositoriesV1:

    @staticmethod
    def get_products() -> QuerySet[models.Product]:
        return models.Product.objects.annotate(min_amount=Min('seller_products__amount', 
                                                       filter=Q(seller_products__is_active=True)))
        

class ProducImageRepositoriesInterface(Protocol):
    
    @staticmethod
    def get_product_images() -> QuerySet[models.ProductImage]:
        ...

class ProductImageRepositoriesV1:

    @staticmethod
    def get_product_images() -> QuerySet[models.ProductImage]:
        return models.ProductImage.objects.all()