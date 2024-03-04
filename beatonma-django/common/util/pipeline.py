from functools import reduce
from typing import Callable, Dict, List, Tuple, TypeVar, Union

T = TypeVar("T")
PipelineFunc = Union[
    Callable[[T], T],  # Single argument function
    Callable[[T, ...], T],  # Multi argument function
]
PipelineItem = Union[
    PipelineFunc,
    Tuple[PipelineFunc, List],  # args
    Tuple[PipelineFunc, List, Dict],  # args, kwargs
]
Pipeline = List[PipelineItem]


def apply_pipeline(receiver: T, pipeline: Pipeline) -> T:
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
        args = item[1] if item_len > 1 else []
        kwargs = item[2] if item_len > 2 else {}

        return func(accumulator, *args, **kwargs)

    return reduce(pipeline_item, pipeline, receiver)
