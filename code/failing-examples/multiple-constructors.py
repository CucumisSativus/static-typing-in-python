class MyClass:
    def __init__(self, attr: int) -> None:
        self.attr = attr

    def __init__(self) -> None:
        self.attr = 10

MyClass(5)