from .base import *  # noqa F403

# GENERAL
# -----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret("SECRET_KEY")  # noqa F405
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = get_secret("ALLOWED_HOSTS")  # noqa F405

# TEMPLATES
# ------------------------------------------------------------------------------
# fix templates.E001 error
TEMPLATES[-1]["APP_DIRS"] = False  # noqa F405
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES[-1]["OPTIONS"]["loaders"] = [  # type: ignore[index] # noqa F405
    (
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    )
]

# CACHES
# -----------------------------------------------------------------------------
# TODO

# SECURITY
# -----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-SECURE_SSL_REDIRECT
# PAW does this redirect automatically
SECURE_SSL_REDIRECT = True
# https://docs.djangoproject.com/en/3.2/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/topics/security/#ssl-https
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-seconds
# TODO: set this to 60 seconds first and then to 518400 once you prove the former works
SECURE_HSTS_SECONDS = 60
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-include-subdomains
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# EMAIL
# -----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"  # noqa F405
# https://docs.djangoproject.com/en/dev/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5
# https://docs.djangoproject.com/en/3.2/ref/settings/#email-host
EMAIL_HOST = get_secret("EMAIL_HOST")  # noqa F405
# https://docs.djangoproject.com/en/3.2/ref/settings/#email-host-user
EMAIL_HOST_USER = get_secret("EMAIL_HOST_USER")  # noqa F405
# https://docs.djangoproject.com/en/3.2/ref/settings/#email-host-password
EMAIL_HOST_PASSWORD = get_secret("EMAIL_HOST_PASSWORD")  # noqa F405
# https://docs.djangoproject.com/en/3.2/ref/settings/#email-port
EMAIL_PORT = get_secret("EMAIL_PORT")  # noqa F405
# https://docs.djangoproject.com/en/3.2/ref/settings/#email-use-tls
EMAIL_USE_TLS = True

# CUSTOM
# -----------------------------------------------------------------------------
MY_PERSONAL_EMAIL = get_secret("MY_PERSONAL_EMAIL")  # noqa F405
# Max allowed size (bytes) of an uploaded image file
IMAGE_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 5  # 5Mb
