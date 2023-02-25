import base58
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from card.models import PurchasedCard, Order, Card
from card.serializers import OrderSerializer, MyCardsSerializer, CardSerializer

from config.settings import STATIC_REVENUE, DYNAMIC_REVENUE
from config.wallet import btc_to_toman, calculate_transaction_fee


class CardCostAPIView(APIView):
    def get(self, request, *args, **kwargs):
        one_btc_toman = btc_to_toman(amount=1, single=True)
        cards = Card.objects.filter(is_active=True)
        data = {
            'btc': one_btc_toman,
            'fee': calculate_transaction_fee(one_btc_toman),
            'dynamic_revenue': DYNAMIC_REVENUE,
            'static_revenue': STATIC_REVENUE,
            'cards': CardSerializer(cards, many=True).data
        }
        return Response(data=data)


class OrderAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user_id=self.request.user.id)


class RetrieveOrderAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_object(self):
        return Order.objects.get(id=self.kwargs['id'], user_id=self.request.user.id)


class MyCardsAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MyCardsSerializer

    def get_queryset(self):
        return PurchasedCard.objects.filter(owner_phone_number=self.request.user.phone_number)


class MyCardAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MyCardsSerializer

    def get_object(self):
        _id = self.kwargs['id']
        if (decoded := base58.b58decode(_id).decode()).find('Gift') == 0:
            _id = decoded[4:]
        return PurchasedCard.objects.get(id=_id, owner_phone_number=self.request.user.phone_number)
