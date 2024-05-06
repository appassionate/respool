from respool.openai import openaiKeyPool, is_openaikey_valid
import pytest



#key file location
_key_file = "tests/keys.yaml"

# load the profiled keys.yaml
keys = openaiKeyPool.from_yaml("keys.yaml")

# pytest to test openai.py

# test is_openaikey_valid


