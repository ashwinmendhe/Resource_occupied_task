from django.contrib import admin
from .models import Resource
# Register your models here.
@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'from_time','to_time', 'date']
