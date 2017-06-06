import functools


undefined = object()


def selfless(cls):
    for key, value in vars(cls).items():
        if callable(value):
            value = add_self(value)
            setattr(cls, key, value)
    return cls


def add_self(function):
    @functools.wraps(function)
    def with_self(self, *args, **kwds):
        scope = function.__globals__
        try:
            old = scope.pop('self', undefined)
            scope['self'] = self
            return function(*args, **kwds)
        finally:
            del scope['self']
            if old is not undefined:
                scope['self'] = old
    return with_self
