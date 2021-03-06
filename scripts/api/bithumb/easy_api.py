from .xcoin_api_client import XCoinAPI
from datetime import datetime

class EasyAPI(XCoinAPI):

    def __init__(self, api_key='', api_secret=''):
        super().__init__(api_key, api_secret)

    #public api
    def get_ticker(self, currency="BTC"):
        """
        get information of last transaction
        거래소 마지막 거래 정보
        parameters
        ----------
        currency: string
            BTC, ETH, DASH, LTC, ETC, XRP, BCH, XMR, ZEC, QTUM, BTG, EOS / ALL
        """

        url = "/public/ticker/{currency}".format(currency=currency)
        result = self.publicCall(url)
        return result

    #public api
    def get_order_book(self, currency="BTC", count=5):
        """
        get order book
        호가 정보
        parameters
        ----------
        currency: string
            BTC, ETH, DASH, LTC, ETC, XRP, BCH, XMR, ZEC, QTUM, BTG, EOS / ALL
        count: integer
        """

        assert count >=1 and count <=50, "count should be between 1 and 50"
        url = "/public/orderbook/{currency}".format(currency=currency)

        params = {
            'count': count
        }
        result = self.publicCall(url, params=params)
        return result

    #public api
    def get_recent_transactions(self, offset = 0, currency="BTC", count=20):
        """
        get recent transcations
        거래소 거래 체결 완료 내역
        parameters
        ----------
        offset: integer
            0~
        currency: string
            BTC, ETH, DASH, LTC, ETC, XRP, BCH, XMR, ZEC, QTUM, BTG, EOS
        count: integer
        """

        assert count >=1 and count <=100, "count should be between 1 and 100"

        url = "/public/recent_transactions/{currency}".format(currency=currency)
        params = {
            'count': count,
            'offset': offset
        }
        result = self.publicCall(url, params=params)
        return result

    #private api
    def get_account(self, currency='BTC'):
        """
        get account info
        회원 정보
        parameters
        ----------
        currency: string
            BTC, ETH, DASH, LTC, ETC, XRP, BCH, XMR, ZEC, QTUM, BTG, EOS
        """
        url = "/info/account"

        p_params = {
            'currency': currency
        }

        result = self.xcoinApiCall(url, p_params=p_params)
        return result

    #private api
    def get_balance(self, currency='ALL'):
        """
        get balance info
        지갑 정보
        parameters
        ----------
        currency: string
            BTC, ETH, DASH, LTC, ETC, XRP, BCH, XMR, ZEC, QTUM, BTG, EOS / ALL
        """
        url = "/info/balance"

        p_params = {
            'currency': currency
        }

        result = self.xcoinApiCall(url, p_params=p_params)
        return result

    #private api
    def get_wallet_address(self, currency='BTC'):
        """
        get wallet_address
        회원 입금 정보
        parameters
        ----------
        currency: string
            BTC, ETH, DASH, LTC, ETC, XRP, BCH, XMR, ZEC, QTUM, BTG, EOS
        """
        url = "/info/wallet_address"

        p_params = {
            'currency': currency
        }

        result = self.xcoinApiCall(url, p_params=p_params)
        return result


    #private api
    def get_my_ticker(self, order_currency='BTC', payment_currency='KRW'):
        """
        get my ticker
        회원 마지막 거래 정보
        parameters
        ----------
        order_currency: string
            BTC, ETH, DASH, LTC, ETC, XRP, BCH, XMR, ZEC, QTUM, BTG, EOS
        payment_currency: string
            KRW
        """
        url = "/info/ticker"

        p_params = {
            'order_currency': order_currency,
            'payment_currency': payment_currency
        }

        result = self.xcoinApiCall(url, p_params=p_params)
        return result

    #private
    def get_my_orders(self, type, count=100, after='2014-11-28 16:40:01', currency='BTC', order_id=None):
        """
        get my orders info
        판/구매 거래 주문 등록 또는 진행 중인 거래
        parameters
        ----------
        type: string
            bid, ask
        after: datetime.datetime, string
            after date 이후의 주문들만 조회
        currency: string
            BTC, ETH, DASH, LTC, ETC, XRP, BCH, XMR, ZEC, QTUM, BTG, EOS
        order_id: string
            판/구매 주문 등록된 주문번호
        """
        url = "/info/orders"

        if isinstance(after, str):
            after = datetime.strptime(after, '%Y-%m-%d %H:%M:%S')

        after_unix = int(after.timestamp()) * 1000

        p_params = {
            'type': type,
            'count': count,
            'after': after_unix,
            'currency': currency,
            'order_id': order_id
        }

        try:
            result = self.xcoinApiCall(url, p_params=p_params)
        except KeyError:
            return None
        return result

    #private
    def get_my_transactions(self, offset=0, count=20, searchGb=0, currency='BTC'):
        """
        get info about my transactions
        회원 거래 내역
        parameters
        ----------
        offset: integer
            0~
        count: integer
        searchGb: integer
            0 : 전체, 1 : 구매완료, 2 : 판매완료, 3 : 출금중, 4 : 입금, 5 : 출금, 9 : KRW입금중
        currency: string
            BTC, ETH, DASH, LTC, ETC, XRP, BCH, XMR, ZEC, QTUM, BTG, EOS
        """
        url = "/info/user_transactions"

        p_params = {
            'offset': offset,
            'count': count,
            'searchGb': searchGb,
            'currency': currency
        }

        result = self.xcoinApiCall(url, p_params=p_params)
        return result

    #private
    def place_limit_order(self, type, order_currency, price, units, payment_currency='KRW'):
        """
        place limit order
        판/구매 거래 주문 등록 및 체결
        parameters
        ----------
        type: string
            bid, ask
        order_currency: string
            BTC, ETH, DASH, LTC, ETC, XRP, BCH, XMR, ZEC, QTUM, BTG, EOS
        price: integer
            price for 1 unit in KRW
        units: float
            order amount
        """
        url = "/trade/place"

        p_params = {
            'type': type,
            'order_currency': order_currency,
            'price': price,
            'units': units,
            'payment_currency': payment_currency
        }

        result = self.xcoinApiCall(url, p_params=p_params)
        return result

    #private
    def get_order_detail(self, type, order_id = None, currency='BTC'):
        """
        get order detail
        parameters
        ----------
        type: string
            bid, ask
        order_id: string
        currency: string
            BTC, ETH, DASH, LTC, ETC, XRP, BCH, XMR, ZEC, QTUM, BTG, EOS
        """
        url = "/info/order_detail"

        p_params = {
            'type': type,
            'order_id': order_id,
            'currency': currency
        }

        result = self.xcoinApiCall(url, p_params=p_params)
        return result

    #private
    def cancel_order(self, type, order_id, currency='BTC'):
        """
        cancel order
        type: string
            bid, ask
        order_id: string
        currency: string
            BTC, ETH, DASH, LTC, ETC, XRP, BCH, XMR, ZEC, QTUM, BTG, EOS
        """
        url = "/trade/cancel"

        p_params = {
            'type': type,
            'order_id': order_id,
            'currency': currency
        }

        result = self.xcoinApiCall(url, p_params=p_params)
        return result

    #private
    def withdraw_currecny(self, units, address, destination, currency='BTC'):
        """
        withdraw currency
        ----------
        units: float
        address: string
        destination: integer(XRP), string
        currency: string
            BTC, ETH, DASH, LTC, ETC, XRP, BCH, XMR, ZEC, QTUM
        """
        url = "/trade/btc_withdrawal"

        p_params = {
            'units': units,
            'address': address,
            'destination': destination,
            'currency': currency
        }

        result = self.xcoinApiCall(url, p_params=p_params)
        return result

    def get_krw_deposit(self):
        """
        get krw deposit info
        KRW 입금 가상계좌 정보 요청
        """
        url = "/trade/krw_deposit"

        result = self.xcoinApiCall(url)
        return result

    def place_market_buy(self, units, currency):
        """
        place market buy
        parameters
        -----------
        units: float
        crrency: string
        """
        url = "/trade/market_buy"

        p_params = {
            'units': units,
            'currency': currency
        }

        result = self.xcoinApiCall(url, p_params=p_params)
        return result

    def place_market_sell(self, units, currency):
        """
        place market sell
        parameters
        ----------
        units: float
        crrency: string
        """
        url = "/trade/market_sell"

        p_params = {
            'units': units,
            'currency': currency
        }

        result = self.xcoinApiCall(url, p_params=p_params)
        return result
