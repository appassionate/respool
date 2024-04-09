# respool
resource pool like ip_proxy openai_keys and etc...


## small install guide
```
git clone [address.git]
pip install -e .
```

## example
### openaiKeyPool:

read yaml file to respool and iterator generating
```python
from respool.openai import openaiKeyPool
pool = openaiKeyPool.from_yaml("./keys.yaml")
iter_cycle = pool.cycle()

#cycle
for i in range(666):
    _key = next(iter_cycle).key
    print("current key is: ", _key)


#misc
# pool._resource
```
keys.yaml
```yaml
- key:  sk-1xxxxxxx
- key:  sk-2xxxxxxx
  freq: 123
```


## resource supporting 

- ipProxyPool: IP proxy
- openaiKeyPool: openai api key for openai sdk or langchain using.

## more feature

1. validation: sync or async(still developing...)
2. iterator generating: providing resource under some principle: cycling, randomly
3. base class for fast developing