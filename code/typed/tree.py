from dataclasses import dataclass
from typing import Union

@dataclass(frozen=True)
class Circle:
    radius: float

@dataclass(frozen=True)
class Rectangle:
    side1: float
    side2: float

Shape = Union[Circle, Rectangle]

def calculate_area(shape: Shape) -> float:
    if isinstance(shape, Circle):
        return shape.radius * shape.radius * 3.14
    else:
        return shape.side1 * shape.side2