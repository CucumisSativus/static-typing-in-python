from dataclasses import dataclass, replace

@dataclass(frozen=True)
class MyClass:
    field1: int
    field2: str

instance = MyClass(1, 'str')

replaced = replace(instance, field1=2)
replaced2 = replace(instance, field1='str') # compiles :(

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