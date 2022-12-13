import os

from celery.schedules import crontab, timedelta


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'django-insecure-83$97y)9(-0eho_b4j7%_%afakk#$3yvu5++@kwf79x7)q7nr$'

DEBUG = int(os.environ.get('DEBUG', 1))

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',

    'apps.users',
    'apps.subscribe_pages',
    'apps.tg_subscribe_pages',
    'apps.payment',
    'apps.partners',
    'apps.stats',
    'apps.api',
    'apps.core',

    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'clearcache',
    'colorfield',
]

AUTH_USER_MODEL = 'users.CustomUser'


MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.locale.LocaleMiddleware',

    'getsub.middlewares.CarrotRequestAuthMiddleware',
    'getsub.middlewares.FormErrorMiddleware'
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

CORS_ALLOWED_ORIGINS = [
    'https://prod-app51446451-59048e70ea30.pages-ac.vk-apps.com',
    'https://user85393911-nn2h2j6c.wormhole.vk-apps.com',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'getsub.permissions.AdminUsernameAPIPermission'
    ]
}

ROOT_URLCONF = 'getsub.urls'

LOGIN_REDIRECT_URL = '/subscribe-pages/'
LOGIN_URL = '/login/'
LOGOUT_REDIRECT_URL = '/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'getsub.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('SQL_ENGINE'),
        'HOST': os.environ.get('SQL_HOST'),
        'NAME': os.environ.get('SQL_NAME'),
        'USER': os.environ.get('SQL_USER'),
        'PASSWORD': os.environ.get('SQL_PASSWORD'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru'
LANGUAGES = (
    ('ru', 'Russian'),
    ('en', 'English')
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, '..', 'static'),
]


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media/')


ISP_URL = os.environ.get('ISP_URL')
ISP_USERNAME = os.environ.get('ISP_USERNAME')
ISP_PASSWORD = os.environ.get('ISP_PASSWORD')

REDIS_HOST = 'redis'
REDIS_PORT = '6379'
REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}'

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_BROKER_URL = REDIS_URL
CELERY_BACKEND_URL = REDIS_URL
CELERY_TASK_SERIALIZER = 'json'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_TIMEZONE = 'UTC'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = REDIS_URL + '/0'
CELERY_RESULT_EXPIRES = 60

BROKER_URL = REDIS_URL
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.yandex.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


UNITPAY_PUBLIC_KEY = os.environ.get('UNITPAY_PUBLIC_KEY')
UNITPAY_SECRET_KEY = os.environ.get('UNITPAY_SECRET_KEY')
UNITPAY_PROJECT_ID = os.environ.get('UNITPAY_PROJECT_ID')

CARROT_REQUEST_USER_AUTH_KEY = os.environ.get('CARROT_REQUEST_USER_AUTH_KEY')
CARROT_REQUEST_AUTH_TOKEN = os.environ.get('CARROT_REQUEST_AUTH_TOKEN')

CENT_API_TOKEN = os.environ.get('CENT_API_KEY')
SHOP_ID = os.environ.get('SHOP_ID')

DOMAIN = os.environ.get("DOMAIN")
LAMADAVA_API_KEY = os.environ.get("LAMADAVA_API_KEY")

API_USERS = [
    'admin',
    'adminAPI',
    'vladyadrov',
]

TELEPORT_BOT_URL = 'https://t.me/Sjjxhskbot'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
CACHE_TTL = 60 * 10