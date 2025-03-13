from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserType(str, Enum):
    student = "Student"
    guest = "Guest"
    admin = "Admin"
    lab_in_charge = "LabInCharge"
    lab_director = "LabDirector"

class UserBase(BaseModel):
    FullName: str
    Email: EmailStr
    ContactNumber: Optional[str] = None
    UserType: UserType

class UserCreate(UserBase):
    password: str

class User(UserBase):
    UserID: int
    
    class Config:
        from_attributes = True

class CredentialsBase(BaseModel):
    AccountStatus: str = "Active"

class CredentialsCreate(CredentialsBase):
    UserID: int
    Password: str

class Credentials(CredentialsBase):
    CredentialID: int
    UserID: int
    LastLogin: Optional[datetime]
    CreatedAt: datetime
    UpdatedAt: datetime
    ResetToken: Optional[str]
    ResetTokenExpiry: Optional[datetime]

    class Config:
        from_attributes = True

class StudentBase(BaseModel):
    StudentNumber: str
    Course: str
    YearLevel: int
    Department: str
    StudentStatus: str = "Regular"

class StudentCreate(StudentBase):
    UserID: int

class Student(StudentBase):
    StudentID: int
    UserID: int
    user: User

    class Config:
        from_attributes = True

class InstructorBase(BaseModel):
    Department: str
    EmployeeID: str
    Position: str
    Specialization: Optional[str] = None
    IsActive: bool = True

class InstructorCreate(InstructorBase):
    UserID: int

class Instructor(InstructorBase):
    InstructorID: int
    UserID: int
    user: User

    class Config:
        from_attributes = True

class GuestBase(BaseModel):
    Organization: str
    Purpose: str
    ValidIDType: str
    ValidIDNumber: str

class GuestCreate(GuestBase):
    UserID: int

class Guest(GuestBase):
    GuestID: int
    UserID: int
    user: User

    class Config:
        from_attributes = True

class AdminBase(BaseModel):
    Role: str

class AdminCreate(AdminBase):
    UserID: int

class Admin(AdminBase):
    AdminID: int
    UserID: int
    user: User

    class Config:
        from_attributes = True

# Token schemas for authentication
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_type: UserType

class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None
    user_type: Optional[UserType] = None
