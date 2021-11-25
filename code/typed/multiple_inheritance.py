class Base1:
    def method(self, attr: int) -> str:
        return f"Base1 method {attr}"

class Base2:
    def method(self, attr: int) -> str:
        return f"Base2 method {attr}"

class MyClass(Base1, Base2):
    pass

print(MyClass().method(10))