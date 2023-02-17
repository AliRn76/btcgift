import json
import requests
import logging
from bit import PrivateKey
from bitcoinaddress import Wallet

from config.settings import DYNAMIC_REVENUE, STATIC_REVENUE
from config.utils import log_warning, log_info

logger = logging.getLogger('root')


def calculate_revenue(amount: float) -> int:
    return int(amount * DYNAMIC_REVENUE) + STATIC_REVENUE


def calculate_transaction_fee(one_btc_toman: float) -> int:
    return int(one_btc_toman * 0.00025)


def calculate_final_cost(amount: float, one_btc_toman: float):
    cost = int(amount * one_btc_toman)
    return cost + calculate_revenue(cost) + calculate_transaction_fee(one_btc_toman)


def btc_to_toman(amount: float | str = None, single: bool = False) -> dict[str, int] | int:
    url = 'https://api.nobitex.ir/v2/orderbook/BTCIRT'
    response = requests.get(url)
    if response.status_code != 200 or (res := json.loads(response.text))['status'] != 'ok':
        log_warning('Nobitex', title='Invalid ًResponse', message=f'{response.status_code} -> {res}')
        return 0

    one_btc_toman = int(res['bids'][0][0]) / 10
    log_info('Nobitex', title='Responded Successfully', message=f'BTC: {one_btc_toman:,}')
    amounts = [
        0.0003, 0.0004, 0.0005, 0.0006, 0.0007, 0.0008, 0.0009,
        0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009,
        0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09,
        0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9,
        1,
    ] if amount is None else [float(amount)]
    if single:
        return calculate_final_cost(amounts[0], one_btc_toman)
    else:
        return {str(a): calculate_final_cost(a, one_btc_toman) for a in amounts}


# print(btc_to_toman(0.0005))


def create_wallet():
    wallet = Wallet()
    print(wallet)


def show_balance():
    print(f'{key.balance=}')


def show_transactions():
    print(f'{key.get_balance()=}')
    print(f'{key.get_transactions()=}')


def create_transaction():
    # 5000 + 10 --> 7580
    # 2420 + 10 --> 5000
    # 0 + 10 --> 2580  # couldn't test but ...

    # 2500 + x --> 8434
    # 1500 + x --> 7434
    # 500  + x --> 6434

    # So 2580Satushi = 0.00002580BTC  is the min fee for now
    transaction = key.send([('1Kgf6erRwKuYT7GbcjfYYGjDVQUfecRdy2', 1, 'satoshi')], fee=10)
    print(f'{transaction=}')
    print(f'{key.get_transactions()=}')
    print(f'{key.get_balance()=}')
    # print(f'{key.get_transactions()=}')
    # print(f'{key.transactions=}')

    # key.create_transaction([('1Archive1n2C579dMsAu3iC6tWzuQJz8dN', 190, 'jpy')])


# key = PrivateKey('5JGPfqxbVH9uYR9v2c9iTFi5N8mu5DsYS3ErEntdz3icoMmmwwN')
