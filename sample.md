class: center, middle
# Static typing (in python)

---

## About me

### Michał Gutowski
* Functional programmer, who landed in python
* Coming from Pabianice, Poland

---

## My story

| <!-- -->    | <!-- -->    |
|-------------|-------------|
| Foo         | Bar         |

---

```python
    def get_latest_user_save_to_db(self):
        user = self.call_external_service()
        user_id = self.save_in_db(user)
        self.report(user_id)
        return user_id
```

Note:
Report only old  users

---

## Agenda

1. type annotations and primitives
1. nominal sub typing
1. data classes
1. new types
1. union types
1. type guards
1. structural polymorphism
1. generics

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

## Nominal sub typing

```python
class Base():
    def method(self) -> str:
        return "str"

class Sub1(Base): pass

class Other: 
    def method(self) -> str:
        return "other str"

def function(obj: Base):
    obj.method()

function(Sub1())
function(Other())
```

```
Argument 1 to "function" has incompatible type "Other"; expected "Base"
```
---

* Public methods in base class are available in the subclass
* Some of the behavior can be overwritten by subclasses
* If not used with caution, can lead to big confusion

---

## Method Resolution Order (MRO) [Link](https://www.python.org/download/releases/2.3/mro/)

```python
class SuperBase1: pass

class SuperBase2: pass

class Base1(SuperBase1): pass

class Base2(SuperBase2): pass

class MyClass(Base1, Base2):pass

print(MyClass.mro())
```

#### Question: what is the order of resolution for MyClass? 
---

```
[<class '__main__.MyClass'>, 
<class '__main__.Base1'>, 
<class '__main__.SuperBase1'>, 
<class '__main__.Base2'>, 
<class '__main__.SuperBase2'>, 
<class 'object'>]
```

Like a tree traversal - always take the the left parent
---

## Abstract Base Classes (ABC) [Link](https://www.python.org/dev/peps/pep-3119/)

```python
from abc import ABC, abstractmethod

class Class(ABC):
    
    @abstractmethod
    def method(self) -> str:
        pass

Class()
```

```
Cannot instantiate abstract class "Class" with abstract attribute "method"
```
---
* Great for describing behavior
* When trying to create an instance of a class, with at least one abstract attribute, we fail

---

## Final [Link](https://www.python.org/dev/peps/pep-0591/)

```python
from typing import final

@final
class Base: pass

class Derived(Base): pass
```
```
Cannot inherit from final class "Base"
```

---

```python
class Base2:
    @final
    def method(self) -> str:
        return ""

class Derived2(Base2):
    def method(self) -> str:
        return super().method()
```

```
Cannot override final attribute "method" 
(previously declared in base class "Base2")
```

---

## Why would you use final?

#### Classes
* to mark that given class is not intended for inheritance
* All the classes intended for inheritance should have a documentation how to do it [link](https://stackoverflow.com/a/218761)
* if you are writing an internal code, and the codebase is not too big - probably an overkill
---


## Data classes

```python
from dataclasses import dataclass, replace

@dataclass(frozen=True)
class MyClass:
    field1: int
    field2: str

instance = MyClass(1, 'str')
```

Dataclasses are product types (`field1` and `field2`)

---

### Sometimes mypy can help

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

### But not always
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

---

### Btw
```python
CompanyId = NewType('Companyid', int)
```

```
error: String argument 1 "Companyid" to NewType(...) 
does not match variable name "CompanyId"
```

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

Union types are sum types (`Admin` or `Employee`)
---

### Union types

* good for modeling data with different shapes
* types do not have to have a common root

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

* You can define polymorphic relation basing on the structure
* You dont need to modify the type - you can use classes from libraries

---
### Structural polymorphism done wrong

```python
class AbstractAVScanner(Protocol):
    @abstractmethod
    def scan(self, contents: str) -> bool:
        pass

def route(scanner: AbstractAVScanner) -> str:
    return f"is file malicious?{scanner.scan('content')}"

class EicarDetector:
    def scan(self, content: str) -> bool:
        return 'eicar' in content

class ActualDetector:
    def __run_av(self, content: str) -> bool:
        # run AV, as a suprocess and take output
        return random() > 0.5

    def scan(self, content: str) -> bool:
        return self.__run_av(content)

route(EicarDetector())
route(ActualDetector())
```

---

```python
class SealDetector:
    def scan(self, contents: str) -> bool:
        return "seal" in contents

route(SealDetector())
```
---
### Structural polymorphism done wrong

* If not paired with new types can really hit hard, when describing behavior
* but it really shines with data

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

### Invariant
---

```python
from typing import TypeVar, Generic

T = TypeVar('T')

class MyList(Generic[T]): pass

class Animal: pass
class Cat(Animal): pass

animal_list: MyList[Animal] = MyList[Animal]()
cats_list: MyList[Animal] = MyList[Cat]()
# Incompatible types in assignment 
# (expression has type "MyList[Cat]", 
# variable has type "MyList[Animal]"
```
---

### Invariant

* `Cat` is `Animal`
* `MyList[Cat]` is not `MyList[Animal]`
* default behaviour - does not care about relation between T and sub or super types

---

### Covariant

```python
from typing import TypeVar, Generic

T = TypeVar('T', covariant=True)

class MyList(Generic[T]): pass

class Animal: pass
class Cat(Animal): pass

animal_list: MyList[Animal] = MyList[Animal]()
cats_list: MyList[Animal] = MyList[Cat]()
```
---
### Covariant
* `Cat` is `Animal`
* `MyList[Cat]` is `MyList[Animal]`
* In mypy all the collections are in covariant

---

### Contravariant
---
```python
T = TypeVar('T', contravariant=True)

class JsonSerializer(Generic[T]):
    def serialize(self, value: T) -> str:
        pass

class Animal: pass
class Cat(Animal): pass

class Controller(Generic[T]):
    def __init__(self, serializer: JsonSerializer[T]) -> None:
        self.__serializer = serializer
    
    def view(self, value: T) -> str:
        return f"Page with {self.__serializer.serialize(value)}"

class AnimalSerializer(JsonSerializer[Animal]):
    def serialize(self, value: Animal) -> str:
        return "Animal"

class CatSerializer(JsonSerializer[Cat]):
    def serialize(self, value: Cat) -> str:
        return "Cat"       

Controller[Cat](CatSerializer())
Controller[Cat](AnimalSerializer())
```
---
### Contravariant

* `Cat` is `Animal` 
* `AnimalSerializer` can serialize `Cat`
* used in `Callable`
* you can pass `Cat` to `Callable[[Animal], int]`