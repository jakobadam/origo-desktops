from django.contrib import admin

from rds.models import (
    Farm,
    FarmPackage,
    Package,
    Server,
    )

class FarmPackageInline(admin.TabularInline):
    model = FarmPackage

class PackageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Package._meta.fields]

class ServerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Server._meta.fields]

class FarmAdmin(admin.ModelAdmin):
    model = Farm
    inlines = [
        FarmPackageInline
    ]


    
admin.site.register(Package, PackageAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(Farm, FarmAdmin)
