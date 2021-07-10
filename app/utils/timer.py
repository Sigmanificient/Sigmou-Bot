import random
from time import perf_counter, sleep
from typing import Dict, Optional, Union, List

keys: Dict[Union[int, str], float] = {}


def time(
        key: Optional[Union[int, str]] = None,
        keep: Optional[bool] = False,
        create: bool = True
) -> Union[bool, float, int, str]:
    """Store a time marker link to a key then return time elapsed from key point."""
    if key is None:
        key: int = hash(random.random())

    if key in keys:
        t_key: float = keys.pop(key) if not keep else keys[key]
        return perf_counter() - t_key

    if create:
        keys[key] = perf_counter()
        return key

    return False


def tests():
    """Checking Timer Performance and Validating."""
    chronos: List[int] = [time() for _ in range(1_000_000)]
    print(len([x for x in chronos if '.' not in str(x)]), 'valid chronometers')

    sleep(1)

    times: List[float] = [time(key) for key in chronos]
    print('first:', times[-1])
    print('last:', times[0])
    print('diff:', abs(times[0] - times[-1]))


if __name__ == '__main__':
    tests()
