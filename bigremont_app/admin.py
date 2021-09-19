from django.contrib import admin

from bigremont_app.models import RemontObject, WorkType, Material

admin.site.register(RemontObject)
admin.site.register(WorkType)
admin.site.register(Material)