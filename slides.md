class: center, middle
# Static typing (in python)

---


## Agenda

1. why static typing
1. what is mypy
1. running and configuring mypy
1. type annotations 
1. special types
1. union types
1. type guards
1. structural polymorphism
1. new types
1. problems with mypy
---

## Type annotations
```python
def function(a: int) -> str:
    return f"{a}"

function("asdf")
```

```
error: Argument 1 to "function" has incompatible type "str"; expected "int"
```

* no type checking happens during runtime
* not annotated functions have type Any

---
### Any

```python
from typing import Any

def function_with_any(argument: Any):
    argument.not_existing_method()

    for a in argument:
        print(a)
    
    argument + 1
```
```
Success: no issues found in 1 source file
```
---
### Any from untyped context

```python
def not_typed(arg):
    pass

def typed(argument: int) -> str:
    return f"arugment={argument}"

typed(not_typed("arg"))
```
```
Success: no issues found in 1 source file
```

---

### Any

* It can be considered a type that has all values and all methods [link](https://www.python.org/dev/peps/pep-0484/#the-any-type)
* It passes the static check, but fails in runtime
* All the functions from untyped context return and accept `Any`
* if mypy is not able to determine typing from import, its `Any`
* `Any` turns off type checking

---

## NoReturn

```python
from typing import NoReturn

def method_without_return() -> NoReturn:
    raise Exception("Boom")
```

No possibility to return

---

### No Return

* Shows that given function do not return anything
* Cannot create an instance of `NoReturn`
* Can be very useful, you will see later

---
## Type inference


```python
def function(a: int) -> str:
    return f"{a}"

def function2(b: int) -> str:
    return f"{b}"

result1 = function(5)
function2(result1)
```

```
error: Argument 1 to "function2" has incompatible type 
"str"; expected "int"
```

???

Even though result1 is not explicitly typed, mypy gets the type right

---

## Union types

```python
from dataclasses import dataclass
from typing import Union

@dataclass(frozen=True)
class Admin:
    email: str
    admin_id: str

@dataclass(frozen=True)
class Employee:
    email: str
    employee_id: str

User = Union[Admin, Employee]

def print_email(user: User):
    if isinstance(user, Admin):
        print(user.email, user.admin_id)
    elif isinstance(user, Employee):
        print(user.email, user.employee_id)

print_email(Admin('admin@admin.ch', 'admin1'))
print_email(Employee('user@user.ch', 'user2'))
```

???

Union types are sum types (`Admin` or `Employee`)
---

### Union types

* good for modeling data with different shapes
* types do not have to have a common root
* types from external libraries can be used here as well

---

## Type guards

```python
from typing import Optional

def add_unsafe(number: Optional[int]) -> int:
    return number + 1
# error: Unsupported operand types for + ("None" and "int")
# note: Left operand is of type "Optional[int]"


def add(number: Optional[int]) -> int:
    if number:
        # mypy knows that number is not None here
        return number + 1
    else:
        return 1
```
---

## Exhaustiveness checking
### Problem

```python
from typing import Union

class Employee: pass
class Manager: pass
class Administrator: pass

User = Union[Employee, Manager, Administrator]

def function(user: User):
    if isinstance(user, Employee):
        print("Employee")
    elif isinstance(user, Manager):
        print("Manager")
Success: no issues found in 1 source file

```
---

### Solution [link](https://github.com/python/typing/issues/735)

```python
def assert_never(x: NoReturn) -> NoReturn:
    raise AssertionError(f"Invalid value: {x!r}")

def function(user: User):
    if isinstance(user, Employee):
        print("Employee")
    elif isinstance(user, Manager):
        print("Manager")
    else:
        assert_never(user)

# error: Argument 1 to "assert_never" 
# has incompatible type "Administrator"; expected "NoReturn"
```
---

## Structural polymorphism - problem

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Admin:
    email: str
    admin_id: str

@dataclass(frozen=True)
class Employee:
    email: str
    employee_id: str

def send_email(with_email: Any):
    print(with_email.email)

send_email(Admin("email", "admin_id"))
send_email(Employee("email", "employee_id"))
send_email(42)
```

???

You can pass both Admin and Employee, no typecheck
---

## Structural polymorphism

```python
from typing import Protocol
from dataclasses import dataclass

class WithEmail(Protocol):
    @property
    def email(self) -> str:
        pass

@dataclass(frozen=True)
class Admin:
    email: str
    admin_id: str

@dataclass(frozen=True)
class Employee:
    email: str
    employee_id: str

def send_email(with_email: WithEmail):
    print(with_email.email)

send_email(Admin("email", "admin_id"))
send_email(Employee("email", "employee_id"))
```
---
## Structural polymorphism

* You can define polymorphic relation basing on the structure
* You dont need to modify the type - you can use classes from libraries
* Great for modeling data and extracting common data pieces from unrelated types
* Big disadvantage is that you cannot track implementations - as opposed to inheritance

---

## New Types

### Problem
```python
order_id = 123
company_id = 3

def find_company_order(company_id: int, order_id: int) -> str:
    return f"company_id={company_id} order_id={order_id}"

print(find_company_order(order_id, company_id))
# => company_id=123 order_id=3

```
---

### Solution
```python
from typing import NewType

OrderId = NewType('OrderId', int)
CompanyId = NewType('CompanyId', int)

order_id = OrderId(123)
company_id = CompanyId(3)
def find_company_order(company_id: CompanyId, order_id: OrderId) -> str:
    return f"company_id={company_id} order_id={order_id}"

find_company_order(order_id, company_id)

# error: Argument 1 to "find_company_order" has incompatible type 
# "OrderId"; expected "CompanyId"
# error: Argument 2 to "find_company_order" has incompatible type 
# "CompanyId"; expected "OrderId"
```
---

### New types

* Add another level of type safety 
* Great for documentation

---
## Sometimes mypy can help

```python
@dataclass(order=True)
class Ordered:
    field1: int
    field2: str

Ordered(1, "a") > Ordered(2, "b")


@dataclass(order=False)
class Unordered:
    field1: int
    field2: str

Unordered(1, 'a') > Unordered(2, 'b')

# Unsupported left operand type for > ("Unordered")
```

---

## But not always
```python
from dataclasses import dataclass, replace

@dataclass(frozen=True)
class MyClass:
    field1: int
    field2: str

instance = MyClass(1, 'str')

replaced = replace(instance, field1=2)
replaced2 = replace(instance, field1='str') # compiles :(
```
---

## When mypy falls short
### Untyped argument

```python
def function_untyped(argument):
    argument.not_existing_method()

    for a in argument:
        print(a)
    
    argument + 1
```
```
Success: no issues found in 1 source file
```

??? 

Because of gradual typing filosophy, it fails siletly

---


## When mypy falls short
### Untyped return

```python
def function_untyped(argument):
    return argument

a = function_untyped(4)
a.not_existing_method("str") + 1

```
```
Success: no issues found in 1 source file
```

??? 

Because of gradual typing filosophy, it fails siletly

---

## When mypy falls short
### Untyped import

```python
import requests
requests.get('https://httpbin.org/basic-auth/user/pass', auth=('user', 'pass'))
```

```
imports.py:1: error: Library stubs not installed for "requests" (or incompatible with Python 3.10)
imports.py:1: note: Hint: "python3 -m pip install types-requests"
imports.py:1: note: (or run "mypy --install-types" to install all missing stub packages)
imports.py:1: note: See https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports
Found 1 error in 1 file (checked 1 source file)
```

???

You can download types if they exist or ignore the issue
---

### Untyped import ignore

```python
import requests # type: ignore
requests.not_existing # obviously fails
```
```
Success: no issues found in 1 source file
```

Note: you can globally ignore certain library in mypy config
---

### With types installed

```python
import requests
requests.not_existing # obviously fails
```

```
imports.py:2: error: Module has no attribute "not_existing"
Found 1 error in 1 file (checked 1 source file)
``` 

---

## When mypy falls short

In all those situations mypy is doing a fallback to *Any* = no type check

* untyped arguments
* untyped return
* import from untyped library (if import error is ignored)

---

