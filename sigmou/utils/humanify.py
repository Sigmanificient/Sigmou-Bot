def format_duration(seconds: int) -> str:
    if not seconds:
        return "now"

    dvr = []
    r = seconds
    for k in (60, 60, 24, 365):
        r, v = divmod(r, k)
        dvr.append(v)

    y, (d, h, m, s) = r, dvr[::-1]

    display = [
        (v, unit)
        for v, unit in zip(
            (y, d, h, m, s),
            ("year", "day", "hour", "minute", "second")
        )
        if v
    ]

    last, last_unit = display.pop()
    suffix = f"{last} {last_unit}{'s' * (last > 1)}"

    if not display:
        return suffix

    return ", ".join(
        f'{v} {d}{"s" * (v > 1)}'
        for v, d in display
    ) + " and " + suffix
