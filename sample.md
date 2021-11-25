---
theme : "solarized"
transition: "slide"
logoImg: "logo.png"
slideNumber: true
title: "Static typing (in python)"
---

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

1. nominal sub typing
1. data classes
1. opaque types
1. union types
1. algebraic data types
1. structural polymorphism
1. generics

---

## Nominal sub typing

```python
class Base():
    def method1(self):
        print("method1 in base")

    def method2(self):
        print("method2 in base")
        self.method1()

class Sub1(Base):
    def method2(self):
        print("method2 in Sub1")
        self.method1()

class Sub2(Base):
    def method1(self):
        print("method1 in sub2")

def function(obj: Base):
    obj.method2()

function(Sub1())
function(Sub2())

```

---

## Constructors are inherited

There is only a single constructor in the class

```python
class Base:
    def __init__(self, attr: int) -> None:
        self.attr = attr

class Sub(Base):
    pass

Base(10).attr
Sub(10).attr
```