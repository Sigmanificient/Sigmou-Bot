second_units = {
    's': 60,
    'm': 60,
    'h': 24,
    'd': 365,
}

sub_second_unit = {
    'ms': 0.001,
    'µs': 0.000001,
    "ns": 0.000000001
}


def pretty_time(time: float) -> str:
    sup = int(time)
    display_units = []

    if sup:
        for unit, equal in second_units.items():
            sup, n = divmod(sup, equal)

            if n:
                display_units.append(f'{n}{unit}')

    if sup:
        display_units.append(f'{sup}y')

    if len(display_units) == 1:
        return display_units[0]

    display_units = display_units[::-1]
    end = display_units.pop()

    return ', '.join(display_units) + f' & {end}'


def pretty_time_small(seconds: float) -> str:
    for unit, eq in sub_second_unit.items():
        if eq < seconds:
            return f"{seconds / eq:,.2f}{unit}"


def main():
    assert pretty_time(1) == '1s'
    assert pretty_time(10) == '10s'

    assert pretty_time(60) == '1m'
    assert pretty_time(3600) == '1h'

    assert pretty_time(86400) == '1d'
    assert pretty_time(31536000) == '1y'

    assert pretty_time(99999999) == '3y, 62d, 9h, 46m & 39s'
    assert pretty_time(31536001) == '1y & 1s'

    assert pretty_time_small(0.1) == '100.00ms'
    assert pretty_time_small(0.005) == '5.00ms'

    assert pretty_time_small(0.0005) == '500.00µs'
    assert pretty_time_small(0.0000005) == '500.00ns'


if __name__ == '__main__':
    main()
