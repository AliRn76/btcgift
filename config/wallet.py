from bitcoinaddress import Wallet
from bit import PrivateKey


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
    transaction = key.send([('...', 1, 'satoshi')], fee=10)
    print(f'{transaction=}')
    print(f'{key.get_transactions()=}')
    print(f'{key.get_balance()=}')
    # print(f'{key.get_transactions()=}')
    # print(f'{key.transactions=}')

    # key.create_transaction([('...', 190, 'jpy')])


key = PrivateKey('5JGPfqxbVH9uYR9v2c9iTFi5N8mu5DsYS3ErEntdz3icoMmmwwN')
