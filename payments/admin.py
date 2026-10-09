from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'collect',
        'user',
        'amount',
        'created_at',
    )
    list_filter = ('created_at',)
    search_fields = (
        'collect__title',
        'user__username',
    )
    readonly_fields = ('created_at',)