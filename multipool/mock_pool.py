
from itertools import starmap

class MockPool:

    closed: bool

    def __init__(self, *args, **kwargs):
        self.closed = False

    def apply(self, func, args=[], kwds={}):
        return func(*args, **kwds)

    def apply_async(self, func, args=[], kwds={}, callback=None, error_callback=None):
        try:
            ret = func(*args, **kwds)
            if callback is not None:
                callback(ret)
        except Exception as e:
            if error_callback is not None:
                error_callback(e)
            return MockResult(None, e)

        return MockResult(ret, None)
    
    def map(self, func, iterable, chunksize=None):
        # TODO return list instead of iterable?
        return map(func, iterable)
    
    def map_async(self, func, iterable, chunksize=None, callback=None, error_callback=None):
        # TODO return list instead of iterable?
        return self.apply_async(map, [func, iterable], callback=callback, error_callback=error_callback)
    
    def imap(self, func, iterable, chunksize=None):
        return map(func, iterable)
    
    def imap_unordered(self, func, iterable, chunksize=None):
        return map(func, iterable)
    
    def starmap(self, func, iterable, chunksize=None):
        return starmap(func, iterable)
    
    def starmap_async(self, func, iterable, chunksize=None, callback=None, error_callback=None):
        return self.apply_async(starmap, [func, iterable], callback=callback, error_callback=error_callback)
    
    def close(self):
        # TODO which error to issue if any function is called after closing
        self.closed = True

    def terminate(self):
        self.closed = True

    def join(self):
        pass

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # TODO what does the original do here?
        self.terminate()
        return False
    


class MockResult:

    def __init__(self, ret=None, exception=None):
        self.ret = ret
        self.exception = exception

    def get(self, timeout=None):
        if self.exception is not None:
            raise self.exception
        else:
            return self.ret
    
    def wait(self, timeout=None):
        pass
    
    def ready(self):
        return True
    
    def successful(self):
        return self.exception is None
    