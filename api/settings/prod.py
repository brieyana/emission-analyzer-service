from .base import *
from urllib.parse import urlparse

DEBUG = False

DB_NAME = os.getenv('POSTGRES_NAME', 'emission-analyzer-db')
DB_USER = os.getenv('POSTGRES_USER', 'user')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB_HOST = os.getenv('POSTGRES_HOST', 'db')
DB_PORT = os.getenv('POSTGRES_PORT', '5432')

DATABASE_URL = f"postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

db_config = urlparse(DATABASE_URL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': db_config.path[1:],
        'USER': db_config.username,
        'PASSWORD': db_config.password,
        'HOST': db_config.hostname,
        'PORT': db_config.port,
    }
}

ALLOWED_HOSTS = ['localhost', '0.0.0.0', '127.0.0.1', 'emission-analyzer-api.vercel.app']
CSRF_TRUSTED_ORIGINS = [
    f'http://localhost:{port}', 'http://127.0.0.1:{port}',
    "https://emission-analyzer-app.vercel.app",
]

CORS_ALLOWED_ORIGINS = [
    f"http://localhost:{port}",
    "https://emission-analyzer-app.vercel.app",
] 

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

