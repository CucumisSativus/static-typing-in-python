from typing import Protocol
from dataclasses import dataclass

class WithEmail(Protocol):
    @property
    def email(self) -> str:
        pass

@dataclass(frozen=True)
class Admin:
    email: str
    admin_id: str

@dataclass(frozen=True)
class Employee:
    email: str
    employee_id: str

def send_email(with_email: WithEmail):
    print(with_email.email)

send_email(Admin("email", "admin_id"))
send_email(Employee("email", "employee_id"))
