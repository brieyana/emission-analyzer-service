from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost']

CORS_ALLOWED_ORIGINS = [
    f"http://localhost:{port}",
]

CSRF_TRUSTED_ORIGINS = [
    f'http://localhost:{port}',
]