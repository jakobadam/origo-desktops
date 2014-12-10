from django.contrib import admin

from rds.models import (
    Package,
    Server,
    )

class PackageAdmin(admin.ModelAdmin):
    readonly_fields = [field.name for field in Package._meta.fields]
    list_display = readonly_fields

class ServerAdmin(admin.ModelAdmin):
    readonly_fields = [field.name for field in Server._meta.fields]
    list_display = readonly_fields

admin.site.register(Package, PackageAdmin)
admin.site.register(Server, ServerAdmin)
