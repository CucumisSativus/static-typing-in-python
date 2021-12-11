from typing import Any

def function_with_any(argument: Any):
    argument.not_existing_method()

    for a in argument:
        print(a)
    
    argument + 1