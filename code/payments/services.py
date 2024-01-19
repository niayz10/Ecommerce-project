import uuid
from typing import Protocol

from django.db import transaction

from . import repositories

from . import models, choices


class BillServicesInterface(Protocol):

    
    def pay_bill(self, bill_id: uuid.UUID) -> None: ...



class BillServicesV1:

    bill_repos: repositories.BillReposInterface = repositories.BillReposV1()
    
    def pay_bill(self, bill_id: uuid.UUID) -> None:
        return self.bill_repos.pay_bill(bill_id=bill_id)