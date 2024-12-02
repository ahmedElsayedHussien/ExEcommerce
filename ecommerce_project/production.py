from .settings import *

DEBUG = False

# Update this with your PythonAnywhere domain
ALLOWED_HOSTS = ['your-username.pythonanywhere.com']

# Static files configuration
STATIC_ROOT = '/home/your-username/ecommerce/static'
MEDIA_ROOT = '/home/your-username/ecommerce/media'

# Security settings
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Database configuration (we'll use MySQL on PythonAnywhere)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your-username$default',
        'USER': 'your-username',
        'PASSWORD': '',  # Set this to your database password
        'HOST': 'your-username.mysql.pythonanywhere-services.com',
    }
}
