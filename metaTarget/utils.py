from functools import wraps
from typing import Callable


def retry(maxAttemptTimes: int):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < maxAttemptTimes:
                res = await func(*args, **kwargs)
                if res != "{}":
                    return res
                else:
                    attempt += 1
            return "{}"
        return wrapper
    return decorator


if __name__ == "__main__":
    @retry(maxAttemptTimes=3)
    def foobar():
        return "{}"


    foobar()
