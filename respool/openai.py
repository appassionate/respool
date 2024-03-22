import tqdm
import numpy as np 
from pydantic import BaseModel
from dataclasses import dataclass

from .base import BaseResourcePool, ResourceStatus
try :
    import openai
except:
    raise ImportError("openai pool need openai package, please install it first.  try 'pip install openai'")


class openaiKey(BaseModel):
    
    state: ResourceStatus = "active"
    key: str
    

def is_openaikey_valid(openai_api_key) -> bool:
    if not openai_api_key:
        return False
    try:
        openai.Client(api_key=openai_api_key).completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt="say hello world."
        )
    except Exception as e:
        return False
    return True


async def is_openaikey_valid_async(openai_api_key) -> bool:
    
    #TODO: 有问题 无法运行

    if not openai_api_key:
        return False
    try:
        await openai.AsyncClient(api_key=openai_api_key).completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt="say hello world."
            )
    
    except Exception as e:
        return False
    return True



class openaiKeyPool(BaseResourcePool):
    
    monomer_type=openaiKey
    
    
    def __init__(self, keys=[], validation=False):
        
        self.reload_data(keys, validation)
    
    @staticmethod
    def _validate_monomer(monomer):
        return is_openaikey_valid(monomer.key)
    
    @staticmethod
    async def _validate_monomer_async(monomer):
        return await is_openaikey_valid_async(monomer.key)
    
    
    # def reload_data(self, data, validation=False):
        
    #     if validation:
    #         self._resource = [key for key in tqdm.tqdm(data) if self._validate_monomer(key)]
    #     else:
    #         self._resource = data
    
    @classmethod
    def from_json(self,filename="openaikeys.json", validation=False):
        return super().from_json(filename=filename, validation=validation)
    
    
    def save_json(self, filename="openaikeys.json"):
        super().save_json(filename=filename)
        