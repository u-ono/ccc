import hmac
import hashlib
import requests
import json
from ccc.utils import make_header, nounce


class CoinCheckClient(object):

    def __init__(self, access_key=None, secret_key=None):
        self.access_key = access_key
        self.secret_key = secret_key

    def get_ticker(self, pair='btc_jpy'):
        """get latest information of coincheck market
        """
        url = 'https://coincheck.com/api/order_books'
        r = requests.get(url, {'pair': pair})

        return json.loads(r.text)

    def get_trades(self, pair='btc_jpy'):
        """get latest deal history of coincheck market
        """
        url = 'https://coincheck.com/api/order_books'
        r = requests.get(url, {'pair': pair})

        return json.loads(r.text)

    def get_orderbooks(self, pair='btc_jpy'):
        """get latest asks/bids information of coincheck market
        """
        url = 'https://coincheck.com/api/order_books'
        r = requests.get(url, {'pair': pair})

        return json.loads(r.text)

    def get_info(self):
        """ show user information
        """
        url = 'https://coincheck.com/api/accounts'
        headers = make_header(url, access_key=self.access_key, secret_key=self.secret_key)
        r = requests.get(url, headers=headers)

        return json.loads(r.text)

    def get_balance(self):
        """ confirm balance
        """
        url = 'https://coincheck.com/api/accounts/balance'
        headers = make_header(url, access_key=self.access_key, secret_key=self.secret_key)
        r = requests.get(url, headers=headers)

        return json.loads(r.text)

    def create_order(self, rate, amount, order_type, pair):
        """ create new order function
        :param rate: float
        :param amount: float
        :param order_type: str; set 'buy' or 'sell'
        :param pair: str; set 'btc_jpy'
        """
        nonce = nounce()
        payload = {'rate': rate,
                   'amount': amount,
                   'order_type': order_type,
                   'pair': pair
                   }
        url = 'https://coincheck.com/api/exchange/orders'
        body = 'rate={rate}&amount={amount}&order_type={order_type}&pair={pair}'.format(**payload)
        message = nonce + url + body
        signature = hmac.new(self.secret_key.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
        headers = {
            'ACCESS-KEY': self.access_key,
            'ACCESS-NONCE': nonce,
            'ACCESS-SIGNATURE': signature
        }
        r = requests.post(url, headers=headers, data=body)
        return json.loads(r.text)

    def get_open_orders(self):
        """ list all open orders func
        """
        url = 'https://coincheck.com/api/exchange/orders/opens'
        headers = make_header(url, access_key=self.access_key, secret_key=self.secret_key)
        r = requests.get(url, headers=headers)
        return json.loads(r.text)

    def cancel(self, order_id):
        """ cancel the specified order
        :param order_id: order_id to be canceled
        """
        url = 'https://coincheck.com/api/exchange/orders/' + order_id
        headers = make_header(url, access_key=self.access_key, secret_key=self.secret_key)
        r = requests.delete(url, headers=headers)
        return json.loads(r.text)

    def get_cancel(self, order_id):
        """ show cancellation status
        :param order_id: order_id to be canceled
        """
        url = 'https://coincheck.com/api/exchange/orders/cancel_status'
        headers = make_header(url, access_key=self.access_key, secret_key=self.secret_key)
        r = requests.get(url, params={'id': order_id}, headers=headers)
        return json.loads(r.text)

    def get_transactions(self):
        """ show payment history
        """
        url = 'https://coincheck.com/api/exchange/orders/transactions'
        headers = make_header(url, access_key=self.access_key, secret_key=self.secret_key)
        r = requests.get(url, headers=headers)
        return json.loads(r.text)
