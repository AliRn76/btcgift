from django.db import models
from card.models import Order
from config.base_manager import BaseManager
from user.models import User


class Transaction(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)
    amount = models.PositiveBigIntegerField(db_column='Amount')
    tracking_id = models.CharField(db_column='TrackingID', max_length=31, blank=True, null=True)
    trx = models.CharField(db_column='trx', max_length=31, blank=True, null=True)
    card_number = models.CharField(db_column='CardNumber', max_length=31, blank=True, null=True)
    is_successful = models.BooleanField(db_column='IsSuccessful', default=False)
    raw_date = models.JSONField(db_column='RawData', blank=True, null=True)
    date_created = models.DateTimeField(db_column='DateCreated', auto_now_add=True)
    order_id = models.ForeignKey(Order, on_delete=models.PROTECT, db_column='OrderID')
    user_id = models.ForeignKey(User, on_delete=models.PROTECT, db_column='UserID')

    objects = BaseManager()

    class Meta:
        db_table = 'Transaction'

    def set_trx(self, trx: str):
        self.trx = trx
        self.save(update_fields=['trx'])

    def submit(self):
        self.is_successful = True
        self.save(update_fields=['is_successful'])
