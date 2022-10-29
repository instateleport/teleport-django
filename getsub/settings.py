from celery.schedules import crontab, timedelta

from decouple import config

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = config('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'apps.users.apps.UsersConfig',
    'apps.subscribe_pages.apps.SubscribePagesConfig',
    'apps.payment.apps.PaymentConfig',
    'apps.partners.apps.PartnersConfig',
    'apps.stats',

    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders'
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
    'https://user85393911-nn2h2j6c.wormhole.vk-apps.com'
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'getsub.permissions.AdminUsernameAPIPermission'
    ]
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=365)
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
}
if eval(os.getenv('IS_SQLITE')):
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
else:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT')
    }


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {

        'ip': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/ip.log'
        },

        'register': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'logs/register.log'
        },

        'domain': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'logs/domain.log'
        },

        'carrot_quest_order_completed': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'logs/carrot_quest/order_completed.log'
        },

        'page': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'logs/page/page-open.log'
        },


    },
    'loggers': {

        'ip': {
            'level': 'INFO',
            'handlers': ['ip'],
            'propagate': True
        },

        'register': {
            'level': 'WARNING',
            'handlers': ['register'],
            'propagate': True
        },

        'domain': {
            'level': 'WARNING',
            'handlers': ['domain'],
            'propagate': True
        },

        'carrot_quest_order_completed': {
            'level': 'WARNING',
            'handlers': ['carrot_quest_order_completed'],
            'propagate': True
        },

        'page': {
            'level': 'WARNING',
            'handlers': ['page'],
            'propagate': True
        },
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
    'locale',
)

TIME_ZONE = config('TIMEZONE')

USE_I18N = True

USE_L10N = True

USE_TZ = True

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
#STATICFILES_DIRS = [
#    os.path.join(BASE_DIR, 'static')
#]

ISP_URL = config('ISP_URL')
ISP_USERNAME = config('ISP_USERNAME')
ISP_PASSWORD = config('ISP_PASSWORD')

REDIS_HOST = config('REDIS_HOST')
REDIS_PORT = config('REDIS_PORT')
REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}'

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_BROKER_URL = REDIS_URL
CELERY_BACKEND_URL = REDIS_URL
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = config('TIMEZONE')
CELERY_RESULT_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = REDIS_URL + '/0'
CELERY_RESULT_EXPIRES = 60

BROKER_URL = REDIS_URL
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}

CELERYBEAT_SCHEDULE = {
    'reset_checks': {
        'task': 'reset_checks',
        'schedule': crontab(hour='23', minute='0')
    },
    'reset_throttled': {
        'task': 'reset_throttled',
        'schedule': crontab(hour='23', minute='0')
    },
    'calculate_and_save_ctr': {
        'task': 'calculate_and_save_ctr',
        'schedule': crontab(minute='5')
    },
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.yandex.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


UNITPAY_PUBLIC_KEY = config('UNITPAY_PUBLIC_KEY')
UNITPAY_SECRET_KEY = config('UNITPAY_SECRET_KEY')
UNITPAY_PROJECT_ID = config('UNITPAY_PROJECT_ID')

CARROT_REQUEST_USER_AUTH_KEY = config('CARROT_REQUEST_USER_AUTH_KEY')
CARROT_REQUEST_AUTH_TOKEN = config('CARROT_REQUEST_AUTH_TOKEN')

CENT_API_TOKEN = config('CENT_API_KEY')
SHOP_ID = config('SHOP_ID')

DOMAIN = config("DOMAIN")
LAMADAVA_API_KEY = config("LAMADAVA_API_KEY")
