
from .settings import *

AUTH_USER_MODEL = "accounts.CustomUser"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db_day8.sqlite3",
    }
}
# Media Configuration
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'EXCEPTION_HANDLER': 'core.exceptions.custom_exception_handler',
}
REST_FRAMEWORK = {
    **REST_FRAMEWORK,
    'DEFAULT_PAGINATION_CLASS': 'core.pagination.CustomPagination',
    'PAGE_SIZE': 5,
}