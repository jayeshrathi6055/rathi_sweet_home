from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from bson import ObjectId
from zoneinfo import ZoneInfo

class UserType(str, Enum):
    EMPLOYEE = 'EMPLOYEE'
    ADMIN = 'ADMIN'
    
class AbsenceType(str, Enum):
    HOLIDAY = 'HOLIDAY'
    LEAVE = 'LEAVE'

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
    leaves: int = 0
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

@dataclass
class EmployeeAbsence:
    _id: ObjectId = None
    user_id: ObjectId = None
    absence_type: AbsenceType = None
    start_date: str = None
    end_date: str = None
