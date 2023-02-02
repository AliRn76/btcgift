import base58
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from card.models import PurchasedCard, Order
from card.serializers import OrderSerializer, MyCardsSerializer
from rest_framework.views import APIView

from config.wallet import btc_to_toman


class CardCostAPIView(APIView):

    def get(self, request, *args, **kwargs):
        amount = self.request.query_params.get('amount')
        return Response(data=btc_to_toman(amount))


class OrderAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user_id=self.request.user.id)


class RetrieveOrderAPIView(ListCreateAPIView, RetrieveAPIView):
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
