from django.contrib import admin

from faq.models import FAQ


class FAQAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'is_active', 'date_created')
    search_fields = ('id', 'title', 'summary', 'description')

    ordering = ('-id',)


admin.site.register(FAQ, FAQAdmin)
