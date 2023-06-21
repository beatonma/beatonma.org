import time
from enum import Enum
from functools import partial, wraps
from typing import List

from django import db

FLOAT_PRECISION_DEFAULT = 2


def dump(
    func=None,
    float_precision: int = FLOAT_PRECISION_DEFAULT,
    queries: bool = False,
    only_on_error: bool = False,
):
    """Print the function call with its resulting value."""

    if func is None:
        return partial(
            dump,
            float_precision=float_precision,
            queries=queries,
            only_on_error=only_on_error,
        )

    @wraps(func)
    def wrapped_func(*args, **kwargs):
        if queries:
            db.reset_queries()

        result = None
        caught_error = None
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            caught_error = e

        if only_on_error is False or (
            only_on_error is True and caught_error is not None
        ):
            print(
                _function_as_string(
                    func, *args, **kwargs, float_precision=float_precision
                )
            )
            print(f"-> {result}")
            if queries:
                print(f"~~ {db_queries_str()}")

            print()

        if caught_error:
            raise caught_error
        return result

    return wrapped_func


def db_queries_str():
    def query_to_string(q: dict):
        query_time = q["time"]
        sql = q["sql"].replace('"', "")

        if query_time == "0.000":
            return f"{sql}"

        return f"({query_time} seconds): {sql}"

    queries = list(db.connection.queries)
    if len(queries) == 0:
        print(
            "connection.queries is empty. If running tests you may need to use --debug-mode cl flag"
        )

    return "\n  ".join([query_to_string(q) for q in queries])


class TimerScale(Enum):
    Nanosecond = 1
    Microsecond = 1000
    Millisecond = 1000000


def timer(func=None, scale: TimerScale = TimerScale.Microsecond):
    if func is None:
        return partial(
            timer,
            scale=scale,
        )

    @wraps(func)
    def wrapped_func(*args, **kwargs):
        start = time.monotonic_ns()
        result = func(*args, **kwargs)
        end = time.monotonic_ns()

        duration_nanoseconds = end - start
        if scale == TimerScale.Nanosecond:
            scaled_duration = duration_nanoseconds
        else:
            scaled_duration = duration_nanoseconds / scale.value

        print(
            f"{_function_as_string(func, *args, **kwargs)} took "
            f"{_float_to_string(scaled_duration)} {scale.name.lower()}s."
        )

        return result

    return wrapped_func


def _function_as_string(
    func,
    *args,
    float_precision: int = FLOAT_PRECISION_DEFAULT,
    **kwargs,
):
    def _dict_to_str(obj: dict) -> List[str]:
        return [f"{key}={value}" for key, value in obj.items()]

    def _to_str(x) -> str:
        if isinstance(x, float):
            return _float_to_string(x, float_precision)
        return str(x)

    all_args = filter(None, [*args, *_dict_to_str(kwargs)])
    all_args = ", ".join([_to_str(x) for x in all_args])

    return f"{func.__name__}({all_args})"


def _float_to_string(value: float, precision: int = FLOAT_PRECISION_DEFAULT):
    return f"{value:.{precision}f}"
