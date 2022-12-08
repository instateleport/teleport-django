from django.conf import settings
import requests

class ISPManagerAPI:
    BASE_URL = settings.ISP_URL
    username = settings.ISP_USERNAME
    password = settings.ISP_PASSWORD

    def add_webdomain(self, domain: str, email: str = None):
        if not email:
            email = f'webmaster@{domain}'
        return requests.get(
            self.BASE_URL +
            f'?authinfo={self.username}:{self.password}'
            f'&func=site.edit&sok=ok'
            f'&site_name={domain}'
            f'&site_aliases='
            f'&site_email={email}'
            f'&site_home=www/instateleport.ru'
            f'&secure=on&site_redirect_http=on'
            f'&site_ssl_cert=ssl_not_used'
            #f'&site_php_mode=php_not_used'
        , verify=False)

    def remove_webdomain(self, domain: str):
        return requests.get(
            self.BASE_URL +
            f'?authinfo={self.username}:{self.password}'
            f'&func=webdomain.delete&elid={domain}'
            f'&remove_directory=off'
            f'&confirm=on'
        , verify=False)

    def set_cert(self, domain: str):
        return requests.get(
            self.BASE_URL +
            f'?authinfo={self.username}:{self.password}'
            f'&func=webdomain.edit&sok=ok'
            f'&elid={domain}'
            f'&ssl_cert={domain}_LE'
        , verify=False)

    def add_cert(self, domain: str):
        # requests.get(
        #     self.BASE_URL +
        #     f'&authinfo={self.username}:{self.password}'
        #     f'&func=sslcert.delete&'
        #     f'&elid={domain}_LE'
        # )
        return requests.get(
            self.BASE_URL +
            f'?authinfo={self.username}:{self.password}'
            f'&func=letsencrypt.generate&sok=ok'
            f'&domain_name={domain}&email=webmaster@{domain}'
            f'&crtname={domain}_LE10&enable_cert=on'
            f'&username=www-root'

            # f'&authinfo={self.username}:{self.password}'
            # f'&func=letsencrypt.generate&sok=ok'
            # f'&domain_name={domain}&domain={domain}'
            # f'&crtname={domain}_LE&enable_cert=on'
        , verify=False)
