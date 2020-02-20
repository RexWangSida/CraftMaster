from django.contrib import admin
from .models import Email
# Register your models here.
class EmailAdmin(admin.ModelAdmin):
    list_display = ('email','register_date')
    ordering = ('register_date')
    search_fields = ('email')
admin.site.register(Email)
