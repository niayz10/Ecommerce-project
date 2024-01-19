from django.db import models

class UserType(models.TextChoices):
    Customer = 'Customer'
    Seller = 'Seller'