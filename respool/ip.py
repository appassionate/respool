from pydantic import BaseModel
from pydantic import BaseModel, Field
from typing import Optional
import asyncio

from .base import BaseResourcePool, ResourceStatus
import httpx
import json

VALIDATION_URL = "https://httpbin.org/ip"

# monomer
class ipProxy(BaseModel):
    
    protocol: str = Field(default="https://")
    ip: str
    port: int
    username: Optional[str]=Field(default=None)
    password: Optional[str]=Field(default=None)
    
    status: ResourceStatus = "active"


def is_ip_valid(ip:ipProxy, timeout=5):
    #sync version
    
    proxy = ip
    #httpx validate proxy resource
    try:
        if proxy.username and proxy.password:
            proxy_account = f"{proxy.username}:{proxy.password}@"
        else:
            proxy_account = ""            
        
        httpx_proxy = {
            f"{proxy.protocol}": f"http://{proxy_account}{proxy.ip}:{proxy.port}"
        }
        with httpx.Client(proxies=httpx_proxy) as client:
            response = client.get(VALIDATION_URL, timeout=timeout)
        
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return False
    
async def is_ip_valid_async(ip:ipProxy, timeout=5):
    
    proxy = ip
    #httpx验证代理资源
    try:
        if proxy.username and proxy.password:
            proxy_account = f"{proxy.username}:{proxy.password}@"
        else:
            proxy_account = ""            
        
        httpx_proxy = {
            f"{proxy.protocol}": f"http://{proxy_account}{proxy.ip}:{proxy.port}"
        }
        async with httpx.AsyncClient(proxies=httpx_proxy) as client:
            response = await client.get(VALIDATION_URL, timeout=timeout)
        
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return False




class ipProxyPool(BaseResourcePool):
    
    monomer_type=ipProxy
    
    def __init__(self, ip_list: list, validation=False) -> None:
        
        self.reload_data(ip_list, validation=validation)
    
    @classmethod
    def from_api(self, api_url, validation=False):
        
        _ips = httpx.get(api_url).json()["data"]
        #print(_ips)
        for _ip in _ips:
            _ip["address"] = _ip["ip"] #useless
        
        return ipProxyPool(_ips, validation=validation)
    
    def save_json(self, filename="ips.json"):
        super().save_json(filename=filename)
    def save_yaml(self, filename="ips.yaml"):
        return super().save_yaml(filename)
    
    
    @staticmethod
    def _validate_monomer(monomer):
        
        proxy = monomer
        return is_ip_valid(proxy, timeout=8)
    
    @staticmethod
    async def _validate_monomer_async(monomer):
        
        proxy = monomer
        return is_ip_valid_async(proxy, timeout=8)
    
    