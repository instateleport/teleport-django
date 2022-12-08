from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

import hashlib
import hmac

import redis


class CarrotRequestAuthMiddleware(MiddlewareMixin):
    def process_template_response(self, request, response):
        if request.user.is_authenticated and 'api/v1/' not in request.path:
            r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
            carrot_quest_hex: bytes = r.hget('carrot_quest_hex', f'{request.user.id}')

            if not carrot_quest_hex:
                carrot_quest_hex = hmac.new(
                    settings.CARROT_REQUEST_USER_AUTH_KEY.encode('utf-8'),
                    str(request.user.id).encode('utf-8'),
                    hashlib.sha256
                ).hexdigest().encode('utf-8')
                r.hset('carrot_quest_hex', f'{request.user.id}', carrot_quest_hex)
            r.close()

            response.context_data['hex'] = carrot_quest_hex.decode('utf-8')
        return response


class FormErrorMiddleware(MiddlewareMixin):
    def process_template_response(self, request, response):

        if 'admin' not in request.path and 'api/v1/' not in request.path:
            form_list = filter(lambda x: x, [
                response.context_data.get('form'),
                response.context_data.get('second_form')
            ])
            if form_list:
                for form in form_list:
                    for field in filter(lambda x: form.errors.get(x), form.fields):
                        field_attrs = form.fields[field].widget.attrs
                        if field_attrs.get('class'):
                            field_attrs['class'] += ' error '
                        else:
                            field_attrs['class'] = 'error'
        return response
