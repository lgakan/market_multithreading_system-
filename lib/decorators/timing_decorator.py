import time
from time import perf_counter, sleep
from functools import wraps
from typing import Callable, Any


def get_time(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time: float = perf_counter()
        result: Any = func(*args, **kwargs)
        end_time: float = perf_counter()
        print(f'"{func.__name__}()" took {end_time - start_time:.3f} seconds to execute')
        return result

    return wrapper


@get_time
def connect() -> None:
    print('Connecting...')
    sleep(2)
    print('Connected!')


def main() -> None:
    connect()


if __name__ == '__main__':
    main()