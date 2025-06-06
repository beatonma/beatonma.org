from functools import reduce
from typing import Callable, Union

type PipelineFunc[T] = Union[
    Callable[[T], T],  # Single argument function
    Callable[[T, ...], T],  # Multi argument function
]
type PipelineItem[T] = Union[
    PipelineFunc[T],
    tuple[PipelineFunc[T], list],  # args
    tuple[PipelineFunc[T], list, dict],  # args, kwargs
]
type Pipeline = list[PipelineItem]


def apply_pipeline[T](receiver: T, pipeline: Pipeline) -> T:
    """Apply each function from the pipeline to the receiver and return the final result.

    Each item in the pipeline may be either:
    - a function
    - a 2-tuple of a function and a list of args
    - a 3-tuple of a function, a list of args, and a dict of kwargs

    Each function will have the result of the previous step as its first argument.
    """

    def pipeline_item(accumulator: T, item: PipelineItem) -> T:
        if callable(item):
            return item(accumulator)

        item_len = len(item)
        func = item[0]
        args = (item[1] if item_len > 1 else None) or []
        kwargs = (item[2] if item_len > 2 else None) or {}

        return func(accumulator, *args, **kwargs)

    return reduce(pipeline_item, pipeline, receiver)
