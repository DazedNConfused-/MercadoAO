from typing import Optional, TypeVar

T = TypeVar("T")


def get_or_else_throw(opt: Optional[T]) -> T:
    """
    Asserts that the given Optional effectively contains a value, and retrieves it.
    Else, it throws an Exception.

    :param opt: The optional to check.
    :return: The unwrapped underlying value.
    """
    if opt is None:
        raise Exception("Expected Optional to contain a value, but was empty!")
    return opt
