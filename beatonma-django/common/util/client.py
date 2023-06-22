from typing import Optional

from django.http import HttpRequest


def get_client_ip(request: HttpRequest) -> Optional[str]:
    real_ip = request.META.get("HTTP_X_REAL_IP")
    if real_ip:
        return real_ip

    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
