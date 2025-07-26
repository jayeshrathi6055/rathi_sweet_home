from dataclasses import dataclass
from datetime import date
from enum import Enum


class UserType(str, Enum):
    EMPLOYEE = 'EMPLOYEE'
    ADMIN = 'ADMIN'

@dataclass
class Employee:
    name: str = None
    age: int = None
    street_address: str = None
    city: str = None
    state: str = None
    date_of_birth: date = None
    salary: int = None
    type: str = UserType.EMPLOYEE
