from typing import Dict, Union, List

second_units: Dict[str, int] = {
    's': 60,
    'm': 60,
    'h': 24,
    'd': 365,
}

sub_second_unit: Dict[str, float] = {
    'ms': 0.001,
    'µs': 0.000001,
    "ns": 0.000000001
}


def pretty_time(time: Union[int, float]) -> str:
    if not time:
        return '0s'

    display_units: List[str] = []

    for unit, equal in second_units.items():
        time, n = divmod(time, equal)

        if n:
            display_units.append(f'{n}{unit}')

        if not time:
            break

    else:
        display_units.append(f'{time}y')

    if len(display_units) == 1:
        return display_units[0]

    display_units = display_units[::-1]
    end = display_units.pop()

    return ', '.join(display_units) + f' & {end}'


def pretty_time_small(seconds: Union[int, float]) -> str:
    for unit, eq in sub_second_unit.items():
        if eq < seconds:
            return f"{seconds / eq:,.2f}{unit}"

    return '0s'
