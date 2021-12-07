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

