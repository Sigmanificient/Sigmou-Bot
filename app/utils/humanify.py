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


def human_time(time: float) -> str:
    sup, sub = divmod(time, 1)
    display_units = []

    if sup:
        for unit, equal in second_units.items():
            sup, n = divmod(sup, equal)

            if n:
                display_units.append(f'{n}{unit}')

    if sup:
        display_units.append(f'{sup}y')

    if sub:
        for unit, equal in sub_second_unit.items():
            n, sub = divmod(sub, equal)

            if n:
                display_units.append(f'{round(n + sub / equal):.0f}{unit}')

    if len(display_units) == 1:
        return display_units[0]

    display_units = display_units[::-1]
    end = display_units.pop()

    return ', '.join(display_units) + f' & {end}'


def main():
    assert human_time(1) == '1s'
    assert human_time(10) == '10s'

    assert human_time(60) == '1m'
    assert human_time(3600) == '1h'

    assert human_time(86400) == '1d'
    assert human_time(31536000) == '1y'

    assert human_time(99999999) == '3y, 62d, 9h, 46m & 39s'
    assert human_time(31536001) == '1y & 1s'

    assert human_time(0.1) == '100ms'
    assert human_time(0.001) == '1ms'

    assert human_time(0.0001) == '100µs'
    assert human_time(0.000001) == '1µs'

    assert human_time(0.0000001) == '100ns'


if __name__ == '__main__':
    main()
