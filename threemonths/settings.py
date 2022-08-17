from pathlib         import Path
from secret_settings import *
from datetime        import timedelta

import pymysql
pymysql.install_as_MySQLdb()



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = SECRET_KEY
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    
    #apps
    'core',
    'users',
    'products',
    'orders',
    
    #third
    'rest_framework',
    'drf_spectacular',
    'corsheaders',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'threemonths.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'threemonths.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = DATABASES

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = False

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

##CORS
CORS_ORIGIN_ALLOW_ALL=True
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}


SIMPLE_JWT = {
    #for test
    'ACCESS_TOKEN_LIFETIME': timedelta(days=100),
    
    #유저속성 중 jwt에 들어갈 필드
    'USER_ID_FIELD': 'id',
    
    #유저속성 중 jwt의 payload에 들어가는 필드의 키값(이름) 예를 들어, user_id라고 하면 payload를 깠을때 user_id라는 키값으로 값이 들어가 있음
    'USER_ID_CLAIM': 'user_id'
    # 'REFRESH_TOKEN_LIFETIME': timedelta(days=60),
    # 'ROTATE_REFRESH_TOKENS': True,
}

AUTH_USER_MODEL = 'users.User'
# AUTH_USER_MODEL = 'core.User'


SPECTACULAR_SETTINGS = {
    'TITLE': 'ThreeMonth API',
    'DESCRIPTION': '서울 빵 다 팔거야!!',
    'VERSION': '1차 배포',
    'SERVE_INCLUDE_SCHEMA': False,
    # OTHER SETTINGS
    'SWAGGER_UI_SETTINGS': {
        # https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/  <- 여기 들어가면 어떤 옵션들이 더 있는지 알수있습니다.
        'dom_id': '#swagger-ui',  # required(default)
        'layout': 'BaseLayout',  # required(default)
        'deepLinking': True,  # API를 클릭할때 마다 SwaggerUI의 url이 변경됨
        'persistAuthorization': True,  # True 이면 SwaggerUI상 Authorize에 입력된 정보가 새로고침을 하더라도 초기화되지 않음
        'displayOperationId': True,  # True이면 API의 urlId 값을 노출 대체로 DRF api name둘과 일치하기때문에 api를 찾을때 유용합니다.
    },
}

#settings.py
# LOGGING = {
#     'disable_existing_loggers': False,
#     'version': 1,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#             'level': 'DEBUG',
#         },
#     },
#     'loggers': {
#         'django.db.backends': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#             'propagate': False,
#         },
#     },
# }

# LOGGING = {
#     'disable_existing_loggers': False,
#     'version': 1,
#     'formatters': {
#         'verbose': {
#             'format': '{asctime} {levelname} {message}',
#             'style': '{'
#         },
#     },
#     'handlers': {
#         'console': {
#             'class'     : 'logging.StreamHandler',
#             'formatter' : 'verbose',
#             'level'     : 'DEBUG',
#         }
#     },
#     'loggers': {
#         'django.db.backends': {
#             'handlers' : ['console'],
#             'level'    : 'DEBUG',
#             'propagate': False,
#         },
#     },
# }


# #ENV 사용법
# from environ import Env
# env = Env()
# env_path = BASE_DIR / ".env"
# if env_path.exists():
#     with env_path.open('rt',encoding='utf8') as f:
#         env.read_env(f,overwrite=True)

# EMAIL_HOST=env.str("EMAIL_HOST")
# EMAIL_PORT=env.int("EMAIL_PORT")
# EMAIL_USE_SSL=env.bool('EMAIL_USE_SSL')
# EMAIL_HOST_USER=env.str('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD=env.str('EMAIL_HOST_PASSWORD')

# DEFAULT_FORM_EMAIL = f"{EMAIL_HOST}@naver.com"