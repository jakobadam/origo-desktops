from django.contrib import admin

from rds.models import (
    Farm,
    FarmPackages,
    Package,
    Server,
    )

class FarmPackagesInline(admin.TabularInline):
    model = FarmPackages

class PackageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Package._meta.fields]

class ServerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Server._meta.fields]

class FarmAdmin(admin.ModelAdmin):
    model = Farm
    inlines = [
        FarmPackagesInline
    ]


    
admin.site.register(Package, PackageAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(Farm, FarmAdmin)
