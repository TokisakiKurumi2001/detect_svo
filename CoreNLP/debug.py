import os


def debug(sent, *args, **kwargs):
    """
    This function only print out if the flag is set. Else ignore
    """
    if os.getenv('DEBUG_FLAG'):
        print(sent, *args, **kwargs)
