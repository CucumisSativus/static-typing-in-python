from dataclasses import dataclass
from typing import Union

@dataclass(frozen=True)
class Admin:
    email: str
    admin_id: str

@dataclass(frozen=True)
class Employee:
    email: str
    employee_id: str

User = Union[Admin, Employee]

def print_email(user: User):
    if isinstance(user, Admin):
        print(user.email, user.admin_id)
    elif isinstance(user, Employee):
        print(user.email, user.employee_id)

print_email(Admin('admin@admin.ch', 'admin1'))
print_email(Employee('user@user.ch', 'user2'))