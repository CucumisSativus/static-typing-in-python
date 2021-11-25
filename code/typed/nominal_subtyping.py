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

print("calling wi")
function(Sub1())
function(Sub2())
