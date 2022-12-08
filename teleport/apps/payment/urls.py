from django.urls import path
from django.shortcuts import HttpResponse

import mimetypes

import os 

from . import views


def verify(request):
    fp = open('5fdeb2b2fb7fc8056420ae0f.txt', "rb")
    response = HttpResponse(fp.read())
    fp.close()
    file_type = mimetypes.guess_type('5fdeb2b2fb7fc8056420ae0f.txt')
    if file_type is None:
        file_type = 'application/octet-stream'
    response['Content-Type'] = file_type
    response['Content-Length'] = str(os.stat('5fdeb2b2fb7fc8056420ae0f.txt').st_size)
    response['Content-Disposition'] = "attachment; filename=5fdeb2b2fb7fc8056420ae0f.txt"
    return response


app_name = 'payment'

urlpatterns = [
    # path('unitpay/handler/', views.payment_handler, name='payment-handler'),
    path('5fdeb2b2fb7fc8056420ae0f.txt/', verify),
    path('unitpay/handler/', views.cent_payment_handler, name='payment-handler'),
]
