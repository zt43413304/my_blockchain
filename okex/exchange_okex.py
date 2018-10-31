import hashlib

import requests


class Exchange_Okex(object):

    def auth(self, api_key, api_secret):
        self._API_KEY = api_key
        self._API_SECRET = api_secret

    def _request(self, method, url, params=None):
        response = None
        if method == 'GET':
            response = requests.get(url, timeout=5)
        else:
            print("The programer gave a wrong http requests method!\n")
        return response.json()

    def get_orderbook(self, symbol, contract_type, size):
        url = "https://www.okex.com/api/v1/future_depth.do?symbol=%s_usdt&contract_type=%s&size=%s" % (
            symbol, contract_type, size)
        return self._request('GET', url)

    def get_sorted_orderbook(self, symbol, contract_type, size):
        raw_orderbook = self.get_orderbook(symbol, contract_type, size)
        sorted_orderbook = {"asks": [], "bids": []}
        length = len(raw_orderbook['asks'])
        for i in range(length):
            sorted_orderbook['asks'].append(raw_orderbook['asks'][length - i - 1])
            sorted_orderbook['bids'].append(raw_orderbook['bids'][i])
        return sorted_orderbook

    def buildMySign(self, params, secretKey):
        sign = ''
        for key in sorted(params.keys()):
            sign += key + '=' + str(params[key]) + '&'
        data = sign + 'secret_key=' + secretKey
        return hashlib.md5(data.encode("utf8")).hexdigest().upper()

    def do_Future_Tx(self, symbol, contract_type, price, amount, trade_type, match_price):
        api_url = "https://www.okex.com/api/v1/future_trade.do"
        post_data = {
            "api_key": self._API_KEY,
            "symbol": symbol + "_usd",
            "contract_type": contract_type,  # this_week, next_week, quarter:
            "price": price,
            "amount": amount,
            "type": trade_type,  # 1:open Long; 2: open Short; 3: close Long 4: close Short
            "match_price": match_price  # buy1 or sell1 price. It match_price is set to 1, then price is not valid.
        }
        post_data['sign'] = self.buildMySign(post_data, self._API_SECRET)
        res = requests.post(api_url, post_data)
        json_res = res.json()
        print(json_res)
        return json_res
