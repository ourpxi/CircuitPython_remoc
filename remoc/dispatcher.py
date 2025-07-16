import json
import random
from . import globals
from .logger import log
import string

def reset_token():
    """Reset the global token to a new random value."""
    chars = string.ascii_letters + string.digits
    globals.token = ''.join(random.choices(chars, k=16))
    log("INFO", "Token Resetted")
    return globals.token

def handlejson(json: str):
    # placeholder for future JSON handling logic
    pass