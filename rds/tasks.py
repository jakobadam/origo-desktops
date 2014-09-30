from __future__ import absolute_import

from celery import shared_task

@shared_task
def message(x):
    print x

@shared_task
def install_package(package, server):
    success = package.deploy(server)
    print package.message
    
