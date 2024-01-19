from typing import Protocol
from django.db.models import QuerySet
from . import models, repositories


class ProductServicesInterface(Protocol):

    def get_products(self) -> QuerySet[models.Product]:
        ...


class ProductServicesV1:
    product_repositories: repositories.ProductRepositoriesInterface = repositories.ProductRepositoriesV1()

    def get_products(self) -> QuerySet[models.Product]:
        return self.product_repositories.get_products()
    

class ProductImageServicesInterface(Protocol):

    def get_product_images(self) -> QuerySet[models.ProductImage]:
        ...


class ProductImageServicesV1:
    product_image_repositories: repositories.ProducImageRepositoriesInterface = repositories.ProductImageRepositoriesV1()

    def get_product_images(self) -> QuerySet[models.ProductImage]:
        return self.product_image_repositories.get_product_images()