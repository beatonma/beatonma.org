from beatonma.settings import environment

WEBMAIL_CONTACT_EMAIL = environment.WEBMAIL_CONTACT_EMAIL
DEFAULT_FROM_EMAIL = environment.EMAIL_HOST_USER


MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.smtp.EmailBackend",
        "OPTIONS": {
            "host": environment.EMAIL_HOST,
            "use_ssl": environment.EMAIL_USE_SSL,
            "use_tls": environment.EMAIL_USE_TLS,
            "username": environment.EMAIL_HOST_USER,
            "password": environment.EMAIL_HOST_PASSWORD,
            "timeout": 10,
        },
    }
}
