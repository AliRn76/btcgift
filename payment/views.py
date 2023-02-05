from django.shortcuts import redirect
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from config.utils import log_info, log_warning
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
        log_info('Payment', title='Verify Transaction', message=f'TransactionID: {transaction_id} Prams: {params}')

        # 1. Check Transaction Exists
        transaction = Transaction.objects.get_or_raise(id=transaction_id)

        # 2. Check Request Params
        if (status := params.get('status', 0)) == 0 or (code := params.get('state_code', 0)) != '99':
            log_warning('Payment', title='Transaction Not Verified', message=f'Status: {status} StatusCode: {code}')
            return redirect(self.redirect_url(success=False, transaction=transaction))

        # 3. Check Transaction trx
        if transaction.trx != (trx := params.get('trx')):
            log_warning('Payment', title='Invalid Transaction trx',
                        message=f'TransactionID: {transaction_id} TRX: {trx}')
            return redirect(self.redirect_url(success=False, transaction=transaction))

        # 4. Check Transaction is_successful
        if transaction.is_successful:
            log_warning('Payment', title='Transaction Was Successful', message=f'TransactionID: {transaction_id}')
            return redirect(self.redirect_url(success=True, transaction=transaction))

        # 5. Verify Transaction With Gateway
        if not Jibimo.verify_transaction(transaction=transaction):
            return redirect(self.redirect_url(success=False, transaction=transaction))

        # 6. Transaction Was Successful
        transaction.succeed()
        log_info('Payment', title='Transaction Verified',
                 message=f'TransactionID: {transaction.id} Amount: {transaction.amount:,}')
        return redirect(self.redirect_url(success=True, transaction=transaction))
