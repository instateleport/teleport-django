from django.conf import settings

from hashlib import sha256
import hashlib

import requests

import urllib.parse
from urllib.request import urlopen

import os

import json

import re

import copy


UNITPAY_PUBLIC_KEY = settings.UNITPAY_PUBLIC_KEY
UNITPAY_SECRET_KEY = settings.UNITPAY_SECRET_KEY
UNITPAY_PROJECT_ID = settings.UNITPAY_PROJECT_ID
# UNITPAY_PUBLIC_KEY='299571-dd2a7'
# UNITPAY_SECRET_KEY='600fcde6c09afe2d1a326e6276649b1e'
# UNITPAY_PROJECT_ID=299571
BASE_URL = 'https://unitpay.ru'
WHITE_LIST_IPs = [
    '31.186.100.49',
    '178.132.203.105',
    '52.29.152.23',
    '52.19.56.234'
]


def parseParams(s):
    params = {}
    for v in s:
        if re.search('params', v):
            p = v[len('params['):-1]
            params[p] = s[v][0]
    return params


# sorted by key
def ksort(d):
    return [[k, d[k]] for k in sorted(d.keys())]


class UnitPay:
    secretKey = ''
    supportedUnitpayMethods = ['initPayment', 'getPayment']
    requiredUnitpayMethodsParams = {'initPayment': ['desc', 'account', 'sum'], 'getPayment': ['paymentId']}
    supportedPartnerMethods = ['check', 'pay', 'error'];
    supportedUnitpayIp = [
        '31.186.100.49',
        '178.132.203.105',
        '52.29.152.23',
        '52.19.56.234',
        '127.0.0.1'  # for debug
    ]

    def __init__(self, domain, secretKey):
        self.formUrl = 'https://' + domain + '/pay/'
        self.apiUrl = 'https://' + domain + '/api'
        self.secretKey = secretKey

    def form(self, publicKey, summ, account, desc, currency='RUB', locale='ru'):
        params = {
            'account': account,
            'currency': currency,
            'desc': desc,
            'sum': summ
        }
        params['signature'] = self.getSignature(params)
        params['locale'] = locale

        return self.formUrl + publicKey + '?' + urllib.parse.urlencode(params)

    def getSignature(self, params, method=None):
        paramss = copy.copy(params)
        if 'signature' in paramss:
            del paramss['signature']
        if 'sign' in paramss:
            del paramss['sign']
        paramss = ksort(paramss)
        paramss.append([0, self.secretKey])
        if method:
            paramss.insert(0, ['method', method])

        # list of dict to str
        res_p = []
        for p in paramss:
            res_p.append(str(p[1]))
        strr = '{up}'.join(res_p)
        strr = strr.encode('utf-8')
        h = hashlib.sha256(strr).hexdigest()
        return h

    def checkHandlerRequest(self):
        ip = os.environ.get('REMOTE_ADDR', '')
        qs = os.environ.get('QUERY_STRING', '')
        val = urllib.parse.parse_qs(qs)
        params = parseParams(val);
        method = val['method'][0]
        if not 'method' in val:
            raise Exception('Method is null')
        if not params:
            raise Exception('Params is null')
        if not method in self.supportedPartnerMethods:
            raise Exception('Method is not supported')
        signature = self.getSignature(params, method);
        if not 'signature' in params:
            raise Exception('signature params is null')
        if params['signature'] != signature:
            raise Exception('Wrong signature')
        if not ip in self.supportedUnitpayIp:
            raise Exception('IP address error')
        return True

    def getErrorHandlerResponse(self, message):
        return json.dumps({'error': {'message': message}})

    def getSuccessHandlerResponse(self, message):
        return json.dumps({'result': {'message': message}})

    def api(self, method, params={}):
        if (not (method in self.supportedUnitpayMethods)):
            raise Exception('Method is not supported')
        for rParam in self.requiredUnitpayMethodsParams[method]:
            if (not rParam in params):
                raise Exception('Param ' + rParam + ' is null')
        params['secretKey'] = self.secretKey
        requestUrl = self.apiUrl + '?method=' + method + '&' + self.insertUrlEncode('params', params)
        response = urlopen(requestUrl)
        data = response.read().decode('utf-8')
        jsons = json.loads(data)
        return jsons

    def insertUrlEncode(self, inserted, params):
        result = ''
        first = True
        for p in params:
            if first:
                first = False
            else:
                result += '&'
            result += inserted + '[' + p + ']=' + str(params[p])
        return result


# def create_payment_url(amount: int, account: str, description: str, currency: str = 'RUB') -> str:
#     hash_str = \
#         str(account) + "{up}" + currency + "{up}" + description + "{up}" + str(amount) + "{up}" + UNITPAY_SECRET_KEY
#     signature = sha256(hash_str.encode()).hexdigest()
#
#     payment_url = BASE_URL + \
#         f'/pay/{UNITPAY_PUBLIC_KEY}?sum={amount}&currency={currency}&account={account}&desc={description}' \
#         f'&signature={signature}'
#     return payment_url


def create_payment_url(order):
    url = 'https://cent.app/api/v1/bill/create'
    headers = {
        'content-type': 'application/json',
        'accept': 'application/json',
        'Authorization': 'Bearer ' + settings.CENT_API_TOKEN
    }

    params = {
        'amount': order.order_sum,
        'description': order.description,
        'order_id': order.order_id,
        'type': 'normal',
        'shop_id': settings.SHOP_ID,
        'currency_in': order.order_currency
    }
    response = requests.post(url, headers=headers, params=params)
    print('response:', response, response.text)
    if response.status_code != 200:
        return False
    else:
        return response.json()
