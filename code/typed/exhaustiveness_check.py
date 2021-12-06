from typing import Union
from typing import NoReturn

class Employee: pass
class Manager: pass
class Administrator: pass

User = Union[Employee, Manager, Administrator]


def assert_never(x: NoReturn) -> NoReturn:
    raise AssertionError(f"Invalid value: {x!r}")

def function(user: User):
    if isinstance(user, Employee):
        print("Employee")
    elif isinstance(user, Manager):
        print("Manager")
    else:
        assert_never(user)

# error: Argument 1 to "assert_never" has incompatible type "Administrator"; expected "NoReturn"
