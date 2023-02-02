import base58
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from config.utils import validate_phone_number
from card.models import Order, PurchasedCard, Card
from config.wallet import btc_to_toman


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['image_front', 'image_back', 'min_amount', 'max_amount']


class MyCardsSerializer(serializers.ModelSerializer):
    image_front = serializers.SerializerMethodField()
    image_back = serializers.SerializerMethodField()

    class Meta:
        model = PurchasedCard
        fields = ['id', 'btc_amount', 'message', 'image_front', 'image_back']

    def absolute_uri(self, url):
        return self.context['request'].build_absolute_uri(url)

    def get_image_front(self, instance):
        return self.absolute_uri(instance.card_id.image_front.url)

    def get_image_back(self, instance):
        return self.absolute_uri(instance.card_id.image_back.url)


class PurchasedCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchasedCard
        exclude = ['previous_owner']
        read_only_fields = ['cost', 'code', 'card_id']

    def validate_owner_phone_number(self, phone_number):
        if (_phone_number := validate_phone_number(phone_number)) is None:
            raise ValidationError('receiver_phone_number not valid')
        return _phone_number


class OrderSerializer(serializers.ModelSerializer):
    card = PurchasedCardSerializer(source='card_id')

    class Meta:
        model = Order
        exclude = ['user_id', 'card_id']
        read_only_fields = ['state']

    def validate_receiver_phone_number(self, phone_number):
        if (_phone_number := validate_phone_number(phone_number)) is None:
            raise ValidationError('receiver_phone_number not valid')
        return _phone_number

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['state'] = 1
        validated_data['user_id'] = user
        btc_amount = validated_data['card_id']['btc_amount']
        purchased_card_count = PurchasedCard.objects.all().count()
        card = PurchasedCard.objects.create(
            **validated_data['card_id'],
            cost=btc_to_toman(btc_amount, single=True),
            code=base58.b58encode(f'Gift{purchased_card_count + 1}'.encode()).decode(),
            card_id=Card.objects.get(min_amount__lte=btc_amount, max_amount__gte=btc_amount),
            previous_owner=user,
        )
        validated_data['card_id'] = card
        return super().create(validated_data)
