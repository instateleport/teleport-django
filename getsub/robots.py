from django.http import HttpResponse
from django.views.decorators.http import require_GET


@require_GET
def robots_txt(request):
    lines = [
        'User-Agent: *',
        'Disallow: /admin',
        'Disallow: *?r=',
        'Disallow: /login',
        'Disallow: /register',
        'Disallow: /privacy-policy',
        'Disallow: /public-offer',
        'Disallow: /reset',
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
