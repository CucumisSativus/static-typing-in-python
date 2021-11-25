class Base:
    def __init__(self, attr: int) -> None:
        self.attr = attr

class Sub(Base):
    pass

Base(10).attr
Sub(10).attr