import os

def ext(file):
    """Returns the file extension
    """
    name, ext = os.path.splitext(file.name)
    return ext.lstrip('.').lower()
