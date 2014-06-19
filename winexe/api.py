from .models import Request

def run(method, **kwargs):
    return Request(method, **kwargs).send()

def cmd(**kwargs):
    return Request('cmd', **kwargs).send()
