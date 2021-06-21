import random
from time import perf_counter, sleep

keys = {}


def time(key=None, keep=False):
    if key is None:
        key = hash(random.random())

    if key in keys:
        t_key = keys.pop(key) if not keep else keys[key]
        return perf_counter() - t_key

    keys[key] = perf_counter()
    return key


def tests():
    chronos = [time() for _ in range(1_000_000)]

    print(len([x for x in chronos if '.' not in str(x)]), 'valid chronometers')

    sleep(1)

    times = [time(key) for key in chronos]
    print('first:', times[-1])
    print('last:', times[0])
    print('diff:', abs(times[0] - times[-1]))


if __name__ == '__main__':
    tests()
