from typing import Protocol, OrderedDict
from . import models
from django.shortcuts import get_object_or_404


class UserRepositoryInterface(Protocol):

    def create_user(self, data: OrderedDict) -> models.CustomUser:
        ...

    def get_user(self, data: OrderedDict) -> models.CustomUser:
        ...


class UserReposotoryV1:
    model = models.CustomUser

    def create_user(self, data: OrderedDict):
        return self.model.objects.create_user(**data)
    
    def get_user(self, data: OrderedDict) -> models.CustomUser:
        user: models.CustomUser = get_object_or_404(self.model, **data)

        # if not user.check_password(data['password']):
        #     raise self.model.DoesNotExist
        
        return user