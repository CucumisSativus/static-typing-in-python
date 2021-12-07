from typing import TypeVar, Generic

T = TypeVar('T', covariant=True)

class MyList(Generic[T]): pass

class Animal: pass
class Dog(Animal): pass
class Cat(Animal): pass

animal_list: MyList[Animal] = MyList[Animal]()
cats_list: MyList[Animal] = MyList[Cat]()