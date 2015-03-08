from .exceptions import NoIndexFound

_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def column_name(index):
    """Return column name for given index"""
    name = ''

    while True:
        q, r = divmod(index, 26)
        name = _chars[r] + name

        if not q:
            return name

        index = q - 1


def column_index(value):
    """Return column index for given name"""

    for index in range(0, 18279):
        name = column_name(index)

        if name == value:
            return index

    raise NoIndexFound


def column_value(value):
    """Return column index or convert from value"""

    if isinstance(value, int):
        return value

    if value.isdigit():
        return int(value)

    return column_index(value)
