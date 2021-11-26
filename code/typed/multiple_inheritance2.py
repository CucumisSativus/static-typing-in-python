class SuperBase1: pass

class SuperBase2: pass

class Base1(SuperBase1): pass

class Base2(SuperBase2): pass

class MyClass(Base1, Base2):pass

print(MyClass.mro())
