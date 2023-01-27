from django.db import models

# from card.models import Buy
from user.models import User


class Wallet(models.Model):
    id = models.BigAutoField(primary_key=True)
    amount = models.BigIntegerField()
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)


# class Transaction(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     date_created = models.DateTimeField()
#     buy_id = models.ForeignKey(Buy, on_delete=models.PROTECT)
#     raw_date = models.JSONField()
#     wallet_id = models.ForeignKey(Wallet, on_delete=models.CASCADE)
#
#     def submit(self):
#         self.buy_id.state = 'Confirmed'
#         self.buy_id.update(updated_fields=['state'])
