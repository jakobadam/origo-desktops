from django.shortcuts import render
from django import http

import subprocess
import os
import rds


from django import http

def test(request):
    collections = rds.collections()
    return http.HttpResponse(str(collections))

if __name__ == '__main__':
    test()
