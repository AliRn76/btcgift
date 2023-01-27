from django.db import models
from user.models import User, Address


class Card(models.Model):
    """
    We should always have cards with 0-1 BTC
        Because we need it in OrderSerializer.create()
    """
    def card_images_path(self, file_name):
        return f'card/{file_name}'

    id = models.BigAutoField(db_column='ID', primary_key=True)
    image = models.ImageField(db_column='Image', upload_to=card_images_path)
    is_active = models.BooleanField(db_column='IsActive', default=True)
    min_amount = models.PositiveIntegerField(db_column='MinAmount')
    max_amount = models.PositiveIntegerField(db_column='MaxAmount')

    class Meta:
        db_table = 'Card'

    def get_image(self):
        return self.image.url


class PurchasedCard(models.Model):
    """
    When someone buy a card for someone else, we put his ID to previous_owner
    and "the" someone else to owner_phone_number
    """
    id = models.BigAutoField(db_column='ID', primary_key=True)
    owner_phone_number = models.CharField(db_column='OwnerPhoneNumber', max_length=31)
    btc_amount = models.FloatField(db_column='BTCAmount')
    code = models.CharField(db_column='Code', max_length=31)  # Generated Code (base58 of Gift{id})
    cost = models.PositiveBigIntegerField(db_column='Cost', help_text='Toman')
    message = models.CharField(db_column='Message', max_length=511, default='', help_text='Text of the message')
    date_updated = models.DateTimeField(db_column='DateUpdated', auto_now=True)
    date_created = models.DateTimeField(db_column='DateCreated', auto_now_add=True)
    card_id = models.ForeignKey(Card, on_delete=models.PROTECT, db_column='CardID')
    previous_owner = models.ForeignKey(User, on_delete=models.PROTECT, db_column='PreviousOwner')

    class Meta:
        db_table = 'PurchasedCard'


class Order(models.Model):
    STATE_CHOICES = (
        (1, 'Processing'),
        (2, 'Creating Wallet'),
        (3, 'Charging Wallet'),
        (4, 'Posting'),
        (5, 'Received'),
        (6, 'Confirmed'),
    )

    id = models.BigAutoField(db_column='ID', primary_key=True)
    state = models.PositiveSmallIntegerField(db_column='State', choices=STATE_CHOICES)
    receiver_name = models.CharField(db_column='ReceiverName', max_length=63)
    receiver_phone_number = models.CharField(db_column='ReceiverPhoneNumber', max_length=31)
    date_updated = models.DateTimeField(db_column='DateUpdated', auto_now=True)
    date_created = models.DateTimeField(db_column='DateCreated', auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.PROTECT, db_column='UserID')
    address_id = models.ForeignKey(Address, on_delete=models.PROTECT, db_column='AddressID')
    card_id = models.ForeignKey(PurchasedCard, on_delete=models.PROTECT, db_column='CardID')

    class Meta:
        db_table = 'Order'

