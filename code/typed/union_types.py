from typing import Union

class Admin: pass

class Employee: pass

User = Union[Admin, Employee]

def handle_login(user: User):
    if isinstance(user, Admin):
        print("Admin login")
    else:
        print("User login")

handle_login(Admin())
handle_login(Employee())