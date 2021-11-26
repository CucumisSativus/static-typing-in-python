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