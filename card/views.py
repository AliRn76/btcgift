from rest_framework.response import Response
from rest_framework.views import APIView

from config.wallet import btc_to_toman


class CardCostAPIView(APIView):

    def get(self, request, *args, **kwargs):
        amount = self.request.query_params.get('amount')
        return Response(data=btc_to_toman(amount))
