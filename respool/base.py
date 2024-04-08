from typing import List
from itertools import cycle, islice
import random
import tqdm
import numpy as np
import asyncio
import json
from enum import Enum

import yaml


# iterator randomly?
def random_iterator(iterable):
    while True:
        yield random.choice(iterable)


def read_yaml(filename):
    with open(filename, "r") as f:
        return yaml.safe_load(f)
    

def save_yaml(data:dict, filename):
    with open(filename, "w") as f:
        yaml.dump(data, f)


class ResourceStatus(Enum):
    
    ACTIVE = 'active'
    EXPIRED = 'expired'
    INACTIVE = 'inactive'


class BaseResourcePool(object):
    
    _resource: List
    monomer_type: object # not implemented in base class
    batch_size = 30
    
    def __getitem__(self, key):
        
        if isinstance(key, slice):
            # 处理切片
            res = self._resource[key.start:key.stop:key.step]
            res = [_mono.dict() for _mono in res]
            _instance = self.__class__(res)
            return _instance
            
        elif isinstance(key, int):
            # 处理整数索引
            res = [self._resource[key]]
            res = [_mono.dict() for _mono in res]
            _instance = self.__class__(res)
            return _instance
        elif isinstance(key, np.ndarray): # 进行蒙版索引
            res = np.array(self._resource)[key]
            res = [_mono.dict() for _mono in res]
            _instance = self.__class__(res)
            return _instance
        
        else:
            raise TypeError("Invalid key type OR Slice type not supported yet.")
    
    
    # generate a resource iterator
    # can iterate the resource evenly using itertools
    def cycle(self):
        return cycle(self._resource)
    
    #randomly iterator 
    def random(self):
        return random_iterator(self._resource)
    
    #TODO: async it 
    @staticmethod
    def _validate_monomer(monomer):
        
        # 1. check if monomer is a valid type
        # 2. special method to validate the resource 
        return NotImplementedError("base class, not implemented")
    
    
    
    def load_validate_func(self, func):
        self._validate_monomer = func
    
    def _validate(self):
        
        res = []
        for key in tqdm.tqdm(self._resource):
            res.append(self._validate_monomer(key))
        
        return np.array(res)
    
    
    async def _validate_async(self):
        
        # _validate_monomer_async是一个异步函数
        tasks = [await self._validate_monomer_async(ip) for ip in self._resource]
        
        return await asyncio.gather(*tasks)
    
    
    def filter_invalid(self):
        
        res = self._validate()
        #print(np.array(self._resource)[res])
        # 非常的臃肿
        return self.__class__([ _mono.dict() for _mono in np.array(self._resource)[res].tolist()])
    
    def reload_data(self, data, validation=False):
        
        if validation:
            print("validating... please wait")
            self._resource = [self.monomer_type(**_mono) for _mono in tqdm.tqdm(data) if self._validate_monomer(_mono)]
        else:
            self._resource = [self.monomer_type(**_mono) for _mono in data]


    def save_json(self, filename="_data.json"):
        with open(filename, "w") as f:
            f.write(json.dumps([_mono.dict() for _mono in self._resource]))
    @classmethod
    def from_json(cls, filename="_data.json", validation=False):
        
        with open(filename, "r") as f:
            _resource = json.load(f)
        return cls(_resource, validation=validation)

    
    def save_yaml(self, filename="_data.yaml"):
        save_yaml([_mono.dict() for _mono in self._resource], filename)
    @classmethod
    def from_yaml(cls, filename="_data.yaml", validation=False):
        
        _resource = read_yaml(filename)
        return cls(_resource, validation=validation)
        