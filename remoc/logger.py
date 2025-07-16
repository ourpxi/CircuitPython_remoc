from . import globals
def set_level(level: str):
    """
    Set the global log level for the logger.

    Args:
        level (str): The log level to set ("DEBUG" or "INFO").
    """
    if level in ("DEBUG", "INFO"):
        globals.log_level = level
        info(f"Log level set to {level}")
    else:
        error(f"Invalid log level: {level}")
def log(level: str, msg: str):
    """
    Logs a message with the specified log level.

    Parameters:
        level (str): The severity level of the log message (e.g., "DEBUG", "INFO", "WARNING", "ERROR").
        msg (str): The message to be logged.
    """ 
    if globals.log_level == "DEBUG":
        print(f"[remoc/{level}] {msg}")
    elif globals.log_level == "INFO" and level != "debug":
        print(f"[remoc/{level}] {msg}")

def info(msg: str):
    log("INFO", msg)

def warning(msg: str):
    log("WARNING", msg)

def error(msg: str):
    log("ERROR", msg)

def debug(msg: str):
    log("DEBUG", msg)