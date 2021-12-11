def not_typed(arg):
    pass

def typed(argument: int) -> str:
    return f"arugment={argument}"

typed(not_typed("arg"))