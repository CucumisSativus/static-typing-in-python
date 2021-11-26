from typing import final

@final
class Base: pass

class Derived(Base): pass

class Base2:
    @final
    def method(self) -> str:
        return ""

class Derived2(Base2):
    def method(self) -> str:
        return super().method()
