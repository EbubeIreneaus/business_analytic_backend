import string
import random

def generateKey(len=10):
    id = "".join(random.choices(string.digits+string.ascii_letters) for _ in range(len))
    return id
