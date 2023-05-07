from warnings import warn


def deprecated(func, message: str | None = None):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""
    if message is None:
        message = f"{func.__name__} function is deprecated."

    def newFunc(*args, **kwargs):
        warn(message, category=DeprecationWarning)
        return func(*args, **kwargs)
    newFunc.__name__ = func.__name__
    newFunc.__doc__ = func.__doc__
    newFunc.__dict__.update(func.__dict__)
    return newFunc
