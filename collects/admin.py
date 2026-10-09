from django.contrib import admin

from .models import Collect


@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'author',
        'occasion',
        'target_amount',
        'end_at',
        'created_at',
    )
    list_filter = ('occasion', 'created_at')
    search_fields = ('title', 'description', 'author__username')
    readonly_fields = ('created_at',)