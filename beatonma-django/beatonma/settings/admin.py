from beatonma.settings import environment

ADMIN_URL = environment.ADMIN_URL
ADMINS = [
    (environment.ADMIN_NAME, environment.ADMIN_EMAIL),
]
DASHBOARD_URL = environment.DASHBOARD_URL
BMA_NOTIFICATIONS_URL = environment.BMA_NOTIFICATIONS_URL
