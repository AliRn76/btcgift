from django.contrib import admin
from card.models import Card, PurchasedCard, Order


class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'min_amount', 'max_amount', 'is_active', 'image_front')


admin.site.register(Card, CardAdmin)
admin.site.register(PurchasedCard)
admin.site.register(Order)

