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
