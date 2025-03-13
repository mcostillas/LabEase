from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class User(Base):
    __tablename__ = "user"

    UserID = Column(Integer, primary_key=True, index=True)
    FullName = Column(String(255), nullable=False)
    Email = Column(String(255), nullable=False)
    ContactNumber = Column(String(11))
    UserType = Column(Enum('Student', 'Guest', 'Admin', 'LabInCharge', 'LabDirector'), nullable=False)

    # Relationships
    credentials = relationship("Credentials", back_populates="user", uselist=False)
    student = relationship("Student", back_populates="user", uselist=False)
    instructor = relationship("Instructor", back_populates="user", uselist=False)
    guest = relationship("Guest", back_populates="user", uselist=False)
    admin = relationship("Admin", back_populates="user", uselist=False)
    bookings = relationship("Booking", back_populates="user")
    notifications = relationship("Notification", back_populates="user")

class Credentials(Base):
    __tablename__ = "credentials"

    CredentialID = Column(Integer, primary_key=True, index=True)
    UserID = Column(Integer, ForeignKey('user.UserID', ondelete='CASCADE'))
    Password = Column(String(255), nullable=False)
    AccountStatus = Column(Enum('Active', 'Inactive', 'Suspended'), default='Active')
    LastLogin = Column(DateTime)
    CreatedAt = Column(DateTime, server_default=func.now())
    UpdatedAt = Column(DateTime, server_default=func.now(), onupdate=func.now())
    ResetToken = Column(String(255))
    ResetTokenExpiry = Column(DateTime)

    # Relationship
    user = relationship("User", back_populates="credentials")

class Student(Base):
    __tablename__ = "student"

    StudentID = Column(Integer, primary_key=True, index=True)
    UserID = Column(Integer, ForeignKey('user.UserID', ondelete='CASCADE'))
    StudentNumber = Column(String(20), nullable=False)
    Course = Column(String(100), nullable=False)
    YearLevel = Column(Integer, nullable=False)
    Department = Column(String(100), nullable=False)
    StudentStatus = Column(Enum('Regular', 'Irregular'), default='Regular')

    # Relationships
    user = relationship("User", back_populates="student")
    attendance_records = relationship("Attendance", back_populates="student")

class Instructor(Base):
    __tablename__ = "instructor"

    InstructorID = Column(Integer, primary_key=True, index=True)
    UserID = Column(Integer, ForeignKey('user.UserID', ondelete='CASCADE'))
    Department = Column(String(100), nullable=False)
    EmployeeID = Column(String(20), nullable=False)
    Position = Column(String(100), nullable=False)
    Specialization = Column(String(255))
    IsActive = Column(Boolean, default=True)

    # Relationships
    user = relationship("User", back_populates="instructor")
    class_schedules = relationship("ClassSchedule", back_populates="instructor")

class Guest(Base):
    __tablename__ = "guest"

    GuestID = Column(Integer, primary_key=True, index=True)
    UserID = Column(Integer, ForeignKey('user.UserID', ondelete='CASCADE'))
    Organization = Column(String(255), nullable=False)
    Purpose = Column(Text, nullable=False)
    ValidIDType = Column(String(50), nullable=False)
    ValidIDNumber = Column(String(50), nullable=False)

    # Relationship
    user = relationship("User", back_populates="guest")

class Admin(Base):
    __tablename__ = "admin"

    AdminID = Column(Integer, primary_key=True, index=True)
    UserID = Column(Integer, ForeignKey('user.UserID', ondelete='CASCADE'))
    Role = Column(String(100), nullable=False)

    # Relationship
    user = relationship("User", back_populates="admin")
