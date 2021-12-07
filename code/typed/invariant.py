from typing import TypeVar, Generic

T = TypeVar('T')

class MyList(Generic[T]): pass

class Animal: pass
class Dog(Animal): pass
class Cat(Animal): pass

animal_list: MyList[Animal] = MyList[Animal]()
cats_list: MyList[Animal] = MyList[Cat]()
# Incompatible types in assignment (expression has type "MyList[Cat]", variable has type "MyList[Animal]"
