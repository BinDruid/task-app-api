from .base import *

DEBUG = False

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, "media/test/")
CELERY_ALWAYS_EAGER = True
