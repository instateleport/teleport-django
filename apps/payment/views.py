from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json
import hashlib

from getsub import settings

from apps.partners.models import Partner
from apps.users.task import order_completed

from .unitpay_api import UnitPay
from . import models


@csrf_exempt
def payment_handler(request) -> HttpResponse:
    unitpay = UnitPay('unitpay.money', settings.UNITPAY_SECRET_KEY)

    data = request.GET
    method = data.get('method')
    answer = json.dumps({})
    if method == 'check':
        answer = unitpay.getSuccessHandlerResponse('Check Success. Ready to pay.')
    elif method == 'pay':
        answer = unitpay.getSuccessHandlerResponse('Pay Success')

        # Order Info
        account = data.get('params[account]')
        order_sum = float(data.get('params[orderSum]'))
        order_currency = data.get('params[orderCurrency]')
        project_id = data['params[projectId]'].strip()

        order = models.Order.objects.get(account=account)
        if (
                order_sum != float(order.order_sum) or
                order_currency != order.order_currency or
                project_id != str(order.project_id)
        ):
            raise Exception('Order validation Error')
        if not order.paid:
            order.paid = True
            order.save(update_fields=['paid'])

            pocket = order.user.pocket
            pocket.balance += order.full_amount
            pocket.save(update_fields=['balance'])

            if order.user.is_referral:
                try:
                    partner = Partner.objects.get(referrals=order.user)
                    partner_channel = order.user.referrer_channel
                    pocket = partner.pocket

                    if partner_channel:
                        partner_channel.earned += order.full_amount * partner.percent / 100
                        partner_channel.save(update_fields=['earned'])

                    pocket.balance += order.full_amount * partner.percent / 100
                    pocket.save(update_fields=['balance'])

                    partner.earned = partner.pocket.balance
                    partner.save(update_fields=['earned'])

                    partner.active_referrals.add(order.user)
                except Partner.DoesNotExist:
                    pass

            order_completed.delay(order.user.id, {
                '$order_id': order.account,
                '$order_id_human': order.user.id,
                '$order_amount': order.order_sum
            })
    elif method == 'error':
        answer = unitpay.getSuccessHandlerResponse('Error logged')
    elif method == 'refund':
        answer = unitpay.getSuccessHandlerResponse('Order canceled')
    return HttpResponse(answer)


@csrf_exempt
def cent_payment_handler(request):
    request_data = request.POST
    response = ''

    order_id = request_data.get('InvId')
    amount = request_data.get('OutSum')
    signature = request_data.get('SignatureValue')
    status = request_data.get("Status")

    try:
        order = models.OrderCent.objects.get(order_id=order_id)
    except models.OrderCent.DoesNotExist as e:
        return HttpResponse(str(e), status=400)

    hash_str = f'{amount}:{order_id}:{settings.CENT_API_TOKEN}'
    signature_to_check = hashlib.md5(hash_str.encode('utf-8')).hexdigest().upper()
    if signature_to_check == signature:
        if status == 'SUCCESS' and float(amount) >= order.order_sum:
            response = 'SUCCESS'

            if not order.paid:
                order.paid = True
                order.save(update_fields=['paid'])

                pocket = order.user.pocket
                pocket.balance += order.full_amount
                pocket.save(update_fields=['balance'])

                order_completed.delay(order.user.id, {
                    '$order_id': order.order_id,
                    '$order_id_human': order.user.id,
                    '$order_amount': order.order_sum
                })

                if order.user.is_referral:
                    try:
                        partner = Partner.objects.get(referrals=order.user)
                        partner_channel = order.user.referrer_channel
                        pocket = partner.pocket

                        if partner_channel:
                            partner_channel.earned += order.full_amount * partner.percent / 100
                            partner_channel.save(update_fields=['earned'])

                        pocket.balance += order.full_amount * partner.percent / 100
                        pocket.save(update_fields=['balance'])

                        partner.earned = partner.pocket.balance
                        partner.save(update_fields=['earned'])

                        partner.active_referrals.add(order.user)
                    except Partner.DoesNotExist:
                        pass
        elif status == 'FAIL':
            response = 'FAIL'
    else:
        response = 'FAIL with signature'
    return HttpResponse(response, status=200)
