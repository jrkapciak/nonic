from django.contrib import admin

from . import models


class BeerAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name", "manufactured_by", "get_styles"]

    def get_styles(self, obj):
        return ", ".join([s.name for s in obj.style.all()])


admin.site.register(models.Beer, BeerAdmin)
admin.site.register(models.Manufacturer)
admin.site.register(models.Style)
