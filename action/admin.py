from django.contrib import admin
from .models import action

@admin.register(action)
class action(admin.ModelAdmin):
    list_display = ('user', 'verb', 'target', 'created')
    list_filter = ('created',)
    search_fields = ('verb',)


