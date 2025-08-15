from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from bson import ObjectId
from zoneinfo import ZoneInfo

class UserType(str, Enum):
    EMPLOYEE = 'EMPLOYEE'
    ADMIN = 'ADMIN'

@dataclass
class Employee:
    _id: ObjectId = None
    name: str = None
    age: int = None
    street_address: str = None
    city: str = None
    state: str = None
    date_of_birth: date = None
    monthly_salary_base: float = None
    monthly_salary_left: float = None
    type: str = UserType.EMPLOYEE
    created_at: str = field(default_factory=lambda : datetime.now(ZoneInfo("Asia/Kolkata")).isoformat())

@dataclass
class EmployeeTransaction:
    _id: ObjectId = None
    user_id: ObjectId = None
    amount: float = None
    created_at: str = field(default_factory=lambda : datetime.now(ZoneInfo("Asia/Kolkata")).isoformat())

@dataclass
class Expense:
    _id: ObjectId = None
    category: str = None
    amount: float = None
    created_at: str = field(default_factory=lambda : datetime.now(ZoneInfo("Asia/Kolkata")).date().isoformat())

@dataclass
class ExpenseCategory:
    _id: ObjectId = None
    category: str = None
