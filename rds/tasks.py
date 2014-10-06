from __future__ import absolute_import

from celery import shared_task

from rds.models import (Package, Server)

@shared_task
def process_upload(package_id):
    package = Package.objects.get(pk=package_id)
    if package.zipped:
        package.unzip()
    package.installer = package.find_installer()
    package.add_dirs()
    package.add_script()
    package.save()    

@shared_task
def install_package(package_id, server_id):
    package = Package.objects.get(pk=package_id)
    server = Server.objects.get(pk=server_id)
    
    res = server.cmd(package.install_cmd, package.args.split())
    success = res.status_code == 0
    if success:
        package.message = 'Deployed %s. %s' % (package,res.std_out)
        package.installed = True
    else:
        package.message = 'Error deploying %s: %s' % (package,res.std_err)
        package.installed = False
    package.save()
