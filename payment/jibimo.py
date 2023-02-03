import json
import requests
from typing import Tuple

from payment.exceptions import GatewayException
from payment.models import Transaction

# from configs.settings import JIBIMO_API_KEY


def _send_request(url: str, header: dict, payload: dict) -> Tuple[dict, int]:
    requests.packages.urllib3.disable_warnings()
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
    try:
        requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
    except AttributeError:
        pass
    try:
        res = requests.post(url, json.dumps(payload), headers=header, verify=False)
    except requests.exceptions.ConnectionError:
        raise GatewayException
    return json.loads(res.text), res.status_code


def request_transaction_url(transaction: Transaction) -> str:
    """
    :param transaction: Transaction
    :return: https://jibimo.com/v2/ipg/redirect/MjM1ODM1
    """

    url = 'https://api.jibimo.com/v2/ipg/request'
    rial_amount = transaction.amount * 10
    header = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-API-KEY': 'JIBIMO_API_KEY',
    }

    payload = {
        'amount': rial_amount,
        'mobile_number': f'+98{transaction.user_id.phone_number}',
        'return_url': f'http://api.btcgift.shop/payment/verify/{transaction.id}/',
        'check_national_code': False,
    }

    response, status_code = _send_request(url=url, payload=payload, header=header)

    if status_code != 200:
        print('*_* {}'.format(response['errors']))
        raise GatewayException

    transaction.set_trx(response['trx'])
    return response['link']


# TODO: Add verify_transaction()