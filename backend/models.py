from sqlalchemy import Column, Integer, String, Enum, Boolean, DateTime, ForeignKey, Text, Time, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "user"

    UserID = Column(Integer, primary_key=True, autoincrement=True)
    FullName = Column(String(255), nullable=False)
    Email = Column(String(100), unique=True, nullable=False)
    ContactNumber = Column(String(20))
    UserType = Column(String(20), nullable=False)  # Admin, Instructor, Student, etc.
    IsActive = Column(Boolean, default=True)

class Instructor(Base):
    __tablename__ = "instructor"

    InstructorID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey('user.UserID', ondelete='CASCADE'))
    Department = Column(String(100))
    EmployeeID = Column(String(20))
    Position = Column(String(100))
    Specialization = Column(String(255))
    IsActive = Column(Boolean, default=True)

    # Relationship
    user = relationship("User")
    class_schedules = relationship("ClassSchedule", back_populates="instructor")

class Laboratory(Base):
    __tablename__ = "laboratory"

    LabID = Column(Integer, primary_key=True, autoincrement=True)
    LabName = Column(String(100), nullable=False)
    Capacity = Column(Integer)

    # Relationship
    class_schedules = relationship("ClassSchedule", back_populates="laboratory")

class Student(Base):
    __tablename__ = "student"

    StudentID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey('user.UserID', ondelete='CASCADE'))
    StudentNumber = Column(String(20), unique=True)
    Course = Column(String(100))
    YearLevel = Column(Integer)
    Department = Column(String(100))
    StudentStatus = Column(String(20))

    # Relationship
    user = relationship("User")
    attendances = relationship("Attendance", back_populates="student")

class ClassSchedule(Base):
    __tablename__ = "class_schedule"

    ClassScheduleID = Column(Integer, primary_key=True, autoincrement=True)
    LabID = Column(Integer, ForeignKey('laboratory.LabID', ondelete='CASCADE'))
    InstructorID = Column(Integer, ForeignKey('instructor.InstructorID', ondelete='CASCADE'))
    DayOfWeek = Column(Enum('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'))
    StartTime = Column(Time, nullable=False)
    EndTime = Column(Time, nullable=False)
    Semester = Column(String(20), nullable=False)
    SchoolYear = Column(String(20), nullable=False)
    Section = Column(String(20), nullable=False)
    IsActive = Column(Boolean, default=True)

    # Relationships
    laboratory = relationship("Laboratory", back_populates="class_schedules")
    instructor = relationship("Instructor", back_populates="class_schedules")
    attendances = relationship("Attendance", back_populates="class_schedule")

class Attendance(Base):
    __tablename__ = "attendance"

    AttendanceID = Column(Integer, primary_key=True, autoincrement=True)
    StudentID = Column(Integer, ForeignKey('student.StudentID', ondelete='CASCADE'))
    ClassScheduleID = Column(Integer, ForeignKey('class_schedule.ClassScheduleID', ondelete='CASCADE'))
    Date = Column(Date, nullable=False)
    TimeIn = Column(Time)
    TimeOut = Column(Time)
    Status = Column(Enum('Present', 'Late', 'Absent', 'Excused'))
    Remarks = Column(Text)

    # Relationships
    student = relationship("Student", back_populates="attendances")
    class_schedule = relationship("ClassSchedule", back_populates="attendances")
