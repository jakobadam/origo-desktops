from django.contrib import admin

from rds.models import (
    Package,
    Server)

admin.site.register(Package)
admin.site.register(Server)
