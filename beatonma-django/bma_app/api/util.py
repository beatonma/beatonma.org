def no_null_dict(**kwargs) -> dict:
    """Create a dictionary with no null values."""
    return {key: value for key, value in kwargs.items() if value is not None}
