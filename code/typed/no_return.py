from typing import NoReturn

def method_without_return() -> NoReturn:
    raise Exception("Boom")

def method_that_returns() -> NoReturn:
    return 1