from django.contrib import admin

from .models import Task, Company

# Campos de solo lectura
#class CompanyAdmin(admin.ModelAdmin):
#    pass


class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('created', ) # coma, espacio) x que es una tupla

# Register your models here.
admin.site.register(Company)

admin.site.register(Task, TaskAdmin)

