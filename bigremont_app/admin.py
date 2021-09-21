from django.contrib import admin

from bigremont_app.models import RemontObject, WorkType, Material, Recipient


class Materialinline(admin.StackedInline):
    model = WorkType.materials.through


class WorkTypeInline(admin.ModelAdmin):
    inlines = (Materialinline,)
    exclude = ('materials', )


admin.site.register(RemontObject)
admin.site.register(Material)
admin.site.register(WorkType, WorkTypeInline)
admin.site.register(Recipient)
