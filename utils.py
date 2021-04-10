from typing import TypeVar, Callable, Tuple


T = TypeVar("T", float, int)


def try_parse(s: str, parse_func: Callable[[str], T], default_func: Callable[[str], T]) -> Tuple[bool, T]:
    if not s or s.isspace():
        return False, default_func(s)

    try:
        return True, parse_func(s)
    except ValueError:
        return False, default_func(s)


def try_parse_int(int_s: str) -> Tuple[bool, int]:
    return try_parse(int_s, lambda s: int(s), lambda s: 0)


def try_parse_float(float_s: str) -> Tuple[bool, float]:
    return try_parse(float_s, lambda s: float(s), lambda s: 0.0)