def pluralize(number: int, one: str, other: str) -> str:
    if number == 1:
        return one
    else:
        return other
