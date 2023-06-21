from inspect import isclass
from typing import Callable, List, Optional, Tuple, Type, Union

from common.views import BaseView
from django.urls import URLPattern
from django.urls import path as django_path


def path(
    route: str,
    view: Union[Type[BaseView], List, Tuple, Callable],
    name: Optional[str] = None,
) -> URLPattern:
    if isclass(view):
        if not name:
            name = getattr(view, "reverse_name", None)
        view = view.as_view()

    return django_path(route, view, name=name)
