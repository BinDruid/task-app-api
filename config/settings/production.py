from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["task.bindruid.ir"]

STATIC_ROOT = os.path.join(BASE_DIR, "public/")
