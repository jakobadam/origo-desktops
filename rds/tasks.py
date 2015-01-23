from __future__ import absolute_import

from celery import shared_task

import logging
import traceback

from rds.models import (Package, Server)
from async_messages.models import Message

log = logging.getLogger(__name__)

@shared_task
def process_upload(package_id):
    try:
        package = Package.objects.get(pk=package_id)
        if package.zipped:
            Message.info(u'Unzipping package "{}"'.format(package))
            package.unzip()
        package.add_dirs()
        package.installer = package.find_installer()
        package.make_executable()
        Message.info(u'Found installer file "{}"'.format(package.installer))
        package.add_script()
        package.save()
    except Exception, e:
        log.error(e)
        log.error(traceback.format_exc())
        Message.error(str(e))

@shared_task
def install_package(package_id, server_id):
    package = Package.objects.get(pk=package_id)
    server = Server.objects.get(pk=server_id)

    res = server.cmd(package.install_cmd)
    success = res.status_code == 0
    if success:
        message = u'Installed "{}". {}'.format(package, res.std_out)
        log.info(package.message)
        Message.success(message)
        package.message = message
        package.installed = True
    else:
        message = u'Error deploying "{}": {}'.format(package, res.std_err)
        log.error(message)
        Message.error(message)
        package.message = message
        package.installed = False

    package.installing = False

    server.updated = True
    server.save()

    package.save()

@shared_task
def uninstall_package(package_id, server_id):
    log.info("TODO uninstall from server?")

    package = Package.objects.get(pk=package_id)

    package.installed = False
    package.save()

@shared_task
def fetch_applications(server_id):
    server = Server.objects.get(pk=server_id)
    try:
        server.fetch_applications()
        message = 'Fetched all applications from the start menu on the RDS server'
        Message.success(message)
        server.updated = False
        server.save()
    except Exception, e:
        Message.error(str(e))
