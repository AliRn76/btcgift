from django.shortcuts import redirect
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from payment.jibimo import Jibimo
from payment.models import Transaction


class PaymentAPIView(APIView):
    permission_classes = [AllowAny]

    def redirect_url(self, success: bool, transaction: Transaction):
        # TODO: Is trx always == tracking_id ? if not --> put tracking_id in redirect_url
        return f'http://btcgift.shop/payment?success={success}&amount={transaction.amount}&tracking_id={transaction.trx}'

    def get(self, request, transaction_id, *args, **kwargs):
        # https://api.btcgift.shop/payment/verify/{transaction_id}/?trx=NTUzNjgw&status=1&state_code=99
        params = self.request.query_params
        print(f'Verify Transaction({transaction_id}) Params: ', params)

        # 1. Check Transaction Exists
        transaction = Transaction.objects.get_or_raise(id=transaction_id)

        # 2. Check Request Params
        if params.get('status', 0) == 0 or params.get('state_code', 0) != '99':
            return redirect(self.redirect_url(success=False, transaction=transaction))

        # 3. Check Transaction trx
        if transaction.trx != params.get('trx'):
            return redirect(self.redirect_url(success=False, transaction=transaction))

        # 4. Check Transaction is_successful
        if transaction.is_successful:
            return redirect(self.redirect_url(success=True, transaction=transaction))

        # 5. Verify Transaction With Gateway
        if not Jibimo.verify_transaction(transaction=transaction):
            return redirect(self.redirect_url(success=False, transaction=transaction))

        # 6. Transaction Was Successful
        transaction.succeed()
        return redirect(self.redirect_url(success=True, transaction=transaction))
