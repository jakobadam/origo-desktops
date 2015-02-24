import os

def ext(filename):
    """Returns the file extension
    """
    name, ext = os.path.splitext(filename)
    return ext.lstrip('.').lower()
