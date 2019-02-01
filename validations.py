"""
    This module contains validations
"""


def non_empty_string(string_arg):

    if not isinstance(string_arg, str):
        raise ValueError("String expected")

    if not string_arg.strip():
        raise ValueError("String should not be empty")

    if string_arg.isdigit():
        raise ValueError("String should not be a number")

    return string_arg
