import json
import random
from . import globals
from .logger import log
import string

def reset_token():
    """Reset the global token to a new random value."""
    chars = string.ascii_letters + string.digits
    globals.token = ''.join(random.choices(chars, k=16))
    log("info ", "Token Resetted")
    return globals.token

def handlejson(raw_json: str) -> str:
    """
    Parses the incoming JSON, verifies auth, and dispatches function calls.
    Expected input format:
    {
        "auth": "token",
        "f1": "func_name",
        "a1": [arg1, arg2],
        "f2": "func_name_2",
        "a2": []
    }

    Returns a JSON string with:
    {
        "auth": "token",
        "f1": "func_name",
        "a1": [...],
        "r1": result1,
        ...
    }
    """
    try:
        data = json.loads(raw_json)
    except Exception:
        log("error", "Invalid JSON format")
        return json.dumps({
            "status": "error",
            "error": "Invalid JSON"
        })

    auth = data.get("auth")
    if auth != globals.token:
        log("error", "Unauthorized access attempt")
        return json.dumps({
            "auth": auth,
            "status": "error",
            "error": "Unauthorized"
        })

    response = {
        "auth": auth
    }

    i = 1
    while True:
        func_key = f"f{i}"
        args_key = f"a{i}"
        ret_key = f"r{i}"

        if func_key not in data:
            break  # no more functions to process

        func_name = data[func_key]
        args = data.get(args_key, [])

        response[func_key] = func_name
        response[args_key] = args

        func = globals.user_functions.get(func_name)

        if not func:
            log("error", f"Function '{func_name}' not found")
            response[ret_key] = f"Error: function '{func_name}' not found"
        else:
            try:
                result = func(*args)
                response[ret_key] = result
                log("info", f"Executed {func_name} → {result}")
            except Exception as e:
                log("error", f"Exception in '{func_name}': {e}")
                response[ret_key] = f"Error: {str(e)}"

        i += 1

    return json.dumps(response)