import json
import requests

from config.utils import log_warning, log_error, log_info
from payment.exceptions import GatewayException
from payment.models import Transaction

# from configs.settings import JIBIMO_API_KEY
JIBIMO_API_KEY = 'XXXX'


class Jibimo:
    request_url = 'https://api.jibimo.com/v2/ipg/request'
    verify_url = 'https://api.jibimo.com/v2/ipg/verify'

    @classmethod
    def _send_request(cls, url: str, payload: dict) -> tuple[dict, int]:
        requests.packages.urllib3.disable_warnings()
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
        try:
            requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
        except AttributeError:
            pass
        header = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-API-KEY': JIBIMO_API_KEY
        }
        try:
            res = requests.post(url=url, data=json.dumps(payload), headers=header, verify=False)
        except requests.exceptions.ConnectionError as e:
            log_error('Jibimo', title='Connection Error')
            raise GatewayException
        if res.status_code != 200:
            log_error('Jibimo', title='Invalid Status', message=f'({res.status_code}) -> {res.content}')
            raise GatewayException
        try:
            return res.json(), res.status_code
        except requests.exceptions.JSONDecodeError as e:
            log_error('Jibimo', title='Invalid Response')
            raise GatewayException

    @classmethod
    def request_transaction_url(cls, transaction: Transaction) -> str:
        """
        :param transaction: Transaction
        :return: https://jibimo.com/v2/ipg/redirect/MjM1ODM1
        """
        rial_amount = transaction.amount * 10
        payload = {
            'amount': rial_amount,
            'mobile_number': f'+98{transaction.user_id.phone_number}',
            'return_url': f'http://api.btcgift.shop/payment/verify/{transaction.id}/',
            'check_national_code': False,
        }
        response, status_code = cls._send_request(url=cls.request_url, payload=payload)
        transaction.set_trx(response['trx'])
        log_info('Jibimo', title='New Transaction URL', message=f'UserID: {transaction.user_id.id} Amount: {transaction.amount:,}')
        return response['link']

    @classmethod
    def verify_transaction(cls, transaction: Transaction) -> bool:
        """
        :param transaction: Transaction
        :return: bool
        """
        payload = {'trx': transaction.trx}
        try:
            response, status_code = cls._send_request(url=cls.verify_url, payload=payload)
        except GatewayException:
            # Something Went Wrong In Gateway
            return False

        """
        {
          "status": 1,
          "state_code": 100,
          "amount": 10000,
          "mobile_number": "+989000000000",
          "card_number": "621986******3238",
          "card_hash": "6BA39385AF1599EB4BFADA1DC3B7A9976DB7B248E93CC4D89237650D472D8391",
          "date": "2021-03-12 20:57:19",
          "card_owner": "محمد محمدی",
          "tracking_id": "MjM1ODMw"
        }
        """
        transaction.verified(response)
        if response.get('status') != 1:
            log_warning('Jibimo', title='Invalid Verifying Status',
                        message=f'Status: {response.get("status")}')
            return False
        return True
