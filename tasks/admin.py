from django.contrib import admin

from .models import Task

# Campos de solo lectura
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('created', ) # coma, espacio) x que es una tupla

# Register your models here.
admin.site.register(Task, TaskAdmin)
