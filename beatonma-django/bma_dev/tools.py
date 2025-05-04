import time
from enum import Enum
from functools import partial, wraps
from typing import Any, Self

from django import db
from django.http import HttpResponse

FLOAT_PRECISION_DEFAULT = 2
INDENT = 0


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
            print(_function_as_string(func, *args, **kwargs))
            print(f"-> {_to_string(result)}")
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


def timer(func=None, scale: TimerScale = TimerScale.Millisecond):
    if func is None:
        return partial(
            timer,
            scale=scale,
        )

    @wraps(func)
    def wrapped_func(*args, **kwargs):
        global INDENT
        INDENT += 2
        start = time.monotonic_ns()
        result = func(*args, **kwargs)
        end = time.monotonic_ns()

        print(
            f"{INDENT * ' '}{_function_as_string(func, *args, **kwargs)} took "
            f"{_format_duration(end - start, scale)}."
        )
        INDENT -= 2

        return result

    return wrapped_func


class Timer:
    label: str
    scale: TimerScale
    print_result: bool

    duration: int
    timers: dict[str, list[Self]]

    # Track timing of internal operations to subtract from measured duration
    overhead: int

    def __init__(
        self,
        label: str = "Timer",
        scale: TimerScale = TimerScale.Millisecond,
        print_result: bool = True,
    ):
        self.label = label
        self.scale = scale
        self.print_result = print_result
        self.duration = None
        self.timers = {}
        self.overhead = 0

    def __enter__(self):
        global INDENT
        INDENT += 2
        self.start = time.monotonic_ns()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.monotonic_ns()
        self.duration = self.end - self.start - self.overhead

        global INDENT
        if self.print_result:
            print(f"{INDENT * ' '}{self}")
        INDENT -= 2

    def sub(self, label: str = "sub"):
        overhead_start = time.monotonic_ns()
        timer = Timer(label=label, print_result=False)

        timers = self.timers.get(label) or []
        timers.append(timer)
        self.timers[label] = timers

        self.overhead += time.monotonic_ns() - overhead_start
        return timer

    def __str__(self):
        return f"{self.label}: {_format_duration(self.duration, self.scale)}"

    def report(self) -> str:
        reports = [self.__str__()]

        for label, timers in self.timers.items():
            count = len(timers)
            mean_duration = sum([x.duration for x in timers]) / count
            reports.append(
                f"  [{label}] (n={count}) x̄={_format_duration(mean_duration, self.scale, show_units=False)}"
            )

        return "\n".join(reports)


def _format_duration(
    duration_nanoseconds, scale: TimerScale, show_units: bool = True
) -> str:
    scaled_duration = duration_nanoseconds / scale.value

    formatted = f"{scaled_duration:.{FLOAT_PRECISION_DEFAULT}f}"
    if show_units:
        formatted += f" {scale.name.lower()}s"
    return formatted


def _function_as_string(
    func,
    *args,
    **kwargs,
):
    def _dict_to_str(obj: dict) -> list[str]:
        return [f"{key}={value}" for key, value in obj.items()]

    all_args = filter(None, [*args, *_dict_to_str(kwargs)])
    all_args = ", ".join([_to_string(x) for x in all_args])

    return f"{func.__name__}({all_args})"


def _to_string(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return f"{value:.{FLOAT_PRECISION_DEFAULT}f}"
    if isinstance(value, HttpResponse):
        return f"{value}: {value.content})"

    return str(value)
