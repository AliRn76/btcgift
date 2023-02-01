from django.db import models


class FAQManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True).order_by('order')


class FAQ(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)
    question = models.CharField(db_column='Question', max_length=255)
    answer = models.TextField(db_column='Answer')
    is_active = models.BooleanField(db_column='IsActive', default=True)
    order = models.PositiveIntegerField(db_column='Order')  # Order in list
    date_updated = models.DateTimeField(db_column='DateUpdated', auto_now=True)
    date_created = models.DateTimeField(db_column='DateCreated', auto_now_add=True)

    objects = models.Manager()
    active = FAQManager()

    class Meta:
        db_table = 'FAQ'

