from django.contrib import admin
from .models import Page
# Register your models here.


# admin page settings for page models

class PageAdmin(admin.ModelAdmin):
    list_display = ('title','update_date')
    ordering = ('title',)
    search_fields = ('title',)
admin.site.register(Page)
