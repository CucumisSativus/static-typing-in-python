class: center, middle
# Static typing (in python)

---

## About me

### Michał Gutowski
* Functional programmer, who landed in python
* Coming from Łódź, Poland

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
1. opaque types
1. union types
1. type guards
1. algebraic data types
1. structural polymorphism
1. generics
1. type guards

---

## Type annotations

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

## Method Resolution Order (MRO) [Link](https://www.python.org/download/releases/2.3/mro/)

```python
class SuperBase1: pass

class SuperBase2: pass

class Base1(SuperBase1): pass

class Base2(SuperBase2): pass

class MyClass(Base1, Base2):pass

print(MyClass.mro())
```

```
[<class '__main__.MyClass'>, 
<class '__main__.Base1'>, 
<class '__main__.SuperBase1'>, 
<class '__main__.Base2'>, 
<class '__main__.SuperBase2'>, 
<class 'object'>]
```

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

## Opaque types

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

## Type guards

```python
from typing import Optional

def add_unsafe(number: Optional[int]) -> int:
    return number + 1
# error: Unsupported operand types for + ("None" and "int")
# note: Left operand is of type "Optional[int]"


def add(number: Optional[int]) -> int:
    if number:
        return number + 1
    else:
        return 1
```