from datetime import datetime, timedelta
from typing import Callable, Tuple, Union

from django.utils import timezone

from common.models import PageView


def cycle_logs(
    older_than: timedelta = timedelta(days=30),
    now: Union[datetime, Callable[[], datetime]] = timezone.now,
) -> Tuple[int, dict]:
    if callable(now):
        now: datetime = now()

    before: datetime = now - older_than
    return PageView.objects.filter(created_at__lte=before).delete()
