from django.contrib import admin

from rds.models import (
    Package,
    Server,
    )

class PackageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Package._meta.fields]

class ServerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Server._meta.fields]

admin.site.register(Package, PackageAdmin)
admin.site.register(Server, ServerAdmin)
