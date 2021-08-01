import random
from time import perf_counter
from typing import Dict, Optional, Union

keys: Dict[Union[str, float], float] = {}


def time(
        key: Optional[Union[float, str]] = None,
        keep: bool = False,
        create: bool = True
) -> Union[bool, float, str]:
    """Store a time marker link to a key
        then return time elapsed from key point."""
    if key is None:
        key: float = random.random()

    if key in keys:
        t_key: float = keys.pop(key) if not keep else keys[key]
        return perf_counter() - t_key

    if create:
        keys[key] = perf_counter()
        return key

    return False
