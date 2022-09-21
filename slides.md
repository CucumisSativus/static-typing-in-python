class: center, middle

# Static type checking in Python
---

## About me

#### Michał Gutowski
#### Software developer at Threatray

---

## Agenda

1. what is mypy
1. type annotations 
1. type inference
1. special types
1. union types
1. type guards
1. structural polymorphism
1. new types
1. generics
1. problems with mypy

---

## What is mypy

> Mypy is a static type checker for Python 3 and Python 2.7. 

* It checks the correctness of the type annotations (PEP 484 and PEP 526)

--

* You can install it with pip 

--

* It can be run on one file, multiple files or recursively over a directory
```
mypy program.py
```
--

* **After type check annotations are no longer used - program is executed as standard python program**

???

I will tell more about type annotations later on
---
## Type annotations
```python
a_variable: int = 3
def function(a: int) -> str:
    return f"{a}"

function("asdf")
```

```
error: Argument 1 to "function" has incompatible type "str"; expected "int"
```

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

## Type inference in classes

```python
class MyClass:
    def __init__(self, attr: int) -> None:
        self.attr = attr


MyClass(10).attr + 'b'
```

```
error: Unsupported operand types for + ("int" and "str")
```

---

## Type inference in class with dynamic context

``` python
class Vicious:
    def just_method(self) -> None:
        self.member = 1

v = Vicious()
v.just_method()
v.member + 's'
```
---

## Type inference in class with dynamic context

```python
class Vicious:
    def just_method(self) -> None:
        self.member = 1
    
    def another_method(self) -> None:
        self.member = 's'
```
```
Incompatible types in assignment 
(expression has type "str", variable has type "int")
```

---
## Possible type annotations

* numbers (`int`, `float`, `Decimal` ...)
* strings
* collections (`List[int]`, `Dict[str, int]`, `Set[int]` ...) - notice upper case name
* our own classes (`BusinessReport`, `CheckoutController`...)
* `None`
* `Optional`
* lambdas (`Callable[[int], str]`)
* special types `Any` and `NoReturn`
* generics

---
## Any

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

## Any

* It can be considered a type that has all values and all methods [link](https://www.python.org/dev/peps/pep-0484/#the-any-type)
* It passes the static check, but fails in runtime
* `Any` turns off type checking

---

## NoReturn


```python
def method_that_returns() -> NoReturn:
    return 1
```

error: Return statement in function which does not return

---

## NoReturn

* Shows that given function do not return anything
* Cannot create an instance of `NoReturn`
* Can be very useful, I will show it later

---
### Middle way conclusion

* you can annotate your code with type annotations

--

* you can check them with mypy

--

* you don't have to type every line - function arguments and returns are enough

---
class: center, middle

## More advanced types
---

## Union types

```python
from dataclasses import dataclass
from typing import Union

@dataclass(frozen=True)
class Circle:
    radius: float

@dataclass(frozen=True)
class Rectangle:
    side1: float
    side2: float

Shape = Union[Circle, Rectangle]

def calculate_area(shape: Shape) -> float:
    if isinstance(shape, Circle):
        return shape.radius * shape.radius * 3.14
    else:
        return shape.side1 * shape.side2
```

???

Union types are sum types (`Admin` or `Employee`)
---

## Union types

* good for modeling data with different shapes (user is either Admin or Employee)
* types do not have to have a common root
* types from external libraries can be used here as well
* as opposed to enum they can have different constructors


---
## Optional
### Problem

```python
def function() -> str:
    return None

function() + "suffix"
```
In runtime

```
TypeError: unsupported operand type(s) for +: 'NoneType' and 'str'
```
--

With mypy
```
error: Incompatible return value type (got "None", expected "str")
```

---
## Optional

* `Optional[T]` is `Union[T, None]`
* Type safe way to indicate that given type can be nullable

---

## Type guards (type narrowing)

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

class Circle: (...)
class Rectangle: (...)
class Triangle: (...) 

Shape = Union[Circle, Rectangle, Triangle]

def function(shape: Shape):
    if isinstance(shape, Circle):
        return "Circle"
    else:
        return "Rectangle"
```
```
Success: no issues found in 1 source file

```
---

## Exhaustiveness checking
### Solution [link](https://github.com/python/typing/issues/735)

```python
def assert_never(x: NoReturn) -> NoReturn:
    raise AssertionError(f"Invalid value: {x!r}")

def function(shape: Shape):
    if isinstance(shape, Circle):
        return "Circle"
    elif isinstance(shape, Rectangle):
        return "Rectangle"
    else:
        assert_never(shape)

# error: Argument 1 to "assert_never" 
# has incompatible type "Triangle"; expected "NoReturn"
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
* You don't need to modify the type - you can use classes from libraries
* Great for modeling data and extracting common data pieces from unrelated types
* More explicit than union types
* Big disadvantage is that you cannot track implementations - as opposed to inheritance

---
## Generics

```python
from typing import TypeVar, Generic

T = TypeVar('T')

class MyList(Generic[T]):
    def append(self, value: T) -> None:
        pass

    def pop(self) -> T:
        pass

intlist = MyList[int]()
intlist.append(5)
value: int = intlist.pop()

intlist.append("str")
# argument 1 to "append" of "MyList" 
# has incompatible type "str"; expected "int"

```
---
### Generics
* used when we want to have a class, that does not care about what is inside
* gives guarantees that `T` is always the same - `MyList[int]` always work with `int`
* generic parameter says `fill this hole to have a complete type`
* you cannot use just `MyList`, its not a complete type
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

## Solution
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

## New types

* Add another level of type safety 
* Great for documentation

---

## Conclusion almost at the end

* When you have multiple types that are exclusive A or B you can use union types

--

* You can use Optional to mark nullable fields for additional safety

--

* Type guards make it easy to work union types

--

* Mypy can check if you really handled all the cases

--

* Protocols allow for a lot of flexibility

--

* Generics can be used when you don't care about the type (but still you care about typing)

--

* New Types are one more level for your safety

---

class: center, middle

## When mypy falls short
---

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

### Untyped import

```python
import requests
requests.get('https://httpbin.org/basic-auth/user/pass', auth=('user', 'pass'))
```

```
error: Library stubs not installed for "requests" (or incompatible with Python 3.10)
note: Hint: "python3 -m pip install types-requests"
note: (or run "mypy --install-types" to install all missing stub packages)
note: See https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports
Found 1 error in 1 file (checked 1 source file)
```

???

You can download types if they exist or ignore the issue
---

## Untyped import ignore

```python
import requests # type: ignore
requests.not_existing # obviously fails
```
```
Success: no issues found in 1 source file
```

Note: you can globally ignore certain library in mypy config
---

## With types installed

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
class: center, middle

## Solution

--

### mypy --strict
---

## Conclusion

* Type checking can spot certain classes of errors
* mypy's type system is flexible and quite sophisticated (union types, type guards and structural polymorphism)
* You can type your application gradually
* But you have to remember that mypy is not doing anything for untyped code fragments