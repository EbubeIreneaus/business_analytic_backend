import string
import random

def generateKey(len=10):
    key = "".join(random.choice(string.digits + string.ascii_letters) for _ in range(len))
    return key
