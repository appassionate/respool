from pydantic import BaseModel
from .base import BaseResourcePool, ResourceStatus
from typing import List, Optional

#only china phone number
class PhoneNumber(BaseModel):

    state: ResourceStatus = "active"
    region: str="86"
    number: str


class PhonePool(BaseResourcePool):
    
    monomer_type=PhoneNumber
    
    def __init__(self, phone_list: list, validation=False) -> None:
        self.reload_data(phone_list, validation=validation)
    
    @staticmethod
    def _validate_monomer(monomer):
        return NotImplementedError("phone pool need to validate the phone number")
    
    
    