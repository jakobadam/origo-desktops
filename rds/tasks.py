from __future__ import absolute_import

from celery import shared_task
from celery.utils.log import get_task_logger

import logging
import traceback

from rds.models import (Package, Server, FarmPackage)
from async_messages.models import Message

log = get_task_logger(__name__)

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
def package_install(farm_package_id, server_id):
    farm_package = FarmPackage.objects.get(pk=farm_package_id)
    package = farm_package.package
    server = Server.objects.get(pk=server_id)

    cmd = package.install_cmd

    try:
        res = server.cmd(cmd)
        success = res.status_code == 0
        if success:
            message = u'Installed "{}" on {}. {}'.format(package, server, res.std_out)
            log.info(package.message)
            Message.success(message)
            farm_package.message = message
            server.updated = True
            farm_package.status = FarmPackage.STATUS_INSTALLED
        else:
            message = u'Error deploying "{}" on {}: {}'.format(package, server, res.std_err)
            log.error(message)
            Message.error(message)
            farm_package.message = message
            farm_package.status = FarmPackage.STATUS_ERROR
    except Exception,e:
        message = u'Error deploying "{}" on {}: {}'.format(package, server, str(e))
        log.error(str(e))
        Message.error(message)

    server.save()
    farm_package.save()

@shared_task
def unpackage_install(package_id, server_id):
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
