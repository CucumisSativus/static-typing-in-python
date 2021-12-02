from typing import Optional

def add_unsafe(number: Optional[int]) -> int:
    return number + 1

def add(number: Optional[int]) -> int:
    if number:
        return number + 1
    else:
        return 1