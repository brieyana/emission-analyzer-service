from .base import *

DEBUG = False

ALLOWED_HOSTS = ['localhost', '0.0.0.0', '127.0.0.1']
CSRF_TRUSTED_ORIGINS = [f'http://localhost:{port}', 'http://127.0.0.1:{port}']

CORS_ALLOWED_ORIGINS = [
    f"http://localhost:{port}",
]

CSRF_TRUSTED_ORIGINS = [
    f'http://localhost:{port}',
]

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

