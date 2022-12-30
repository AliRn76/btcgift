from django.db import models
from user.models import User, Address


class Card(models.Model):
    def card_images_path(self, file_name):
        return f'card/{file_name}'

    id = models.BigAutoField(db_column='ID', primary_key=True)
    image = models.ImageField(db_column='Image', upload_to=card_images_path)
    min_amount = models.PositiveIntegerField(db_column='MinAmount')
    max_amount = models.PositiveIntegerField(db_column='MaxAmount')


class Buy(models.Model):
    STATE_CHOICES = (
        (1, 'Confirmed'),
    )

    id = models.BigAutoField(db_column='ID', primary_key=True)
    amount = models.PositiveIntegerField(db_column='Amount', )
    state = models.PositiveSmallIntegerField(db_column='State', choices=STATE_CHOICES)
    date_created = models.DateTimeField(db_column='DateCreated', auto_now_add=True)
    card_id = models.ForeignKey(Card, db_column='CardID', on_delete=models.PROTECT)
    user_id = models.ForeignKey(User, db_column='UserID', on_delete=models.PROTECT)
    address_id = models.ForeignKey(Address, db_column='AddressID', on_delete=models.PROTECT)
