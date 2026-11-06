
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
