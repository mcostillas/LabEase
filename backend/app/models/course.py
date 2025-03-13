from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, Date, Time, Enum
from sqlalchemy.orm import relationship
from ..database import Base

class Course(Base):
    __tablename__ = "course"

    CourseID = Column(Integer, primary_key=True, index=True)
    CourseCode = Column(String(20), unique=True, nullable=False)
    CourseName = Column(String(255), nullable=False)
    Department = Column(String(100), nullable=False)
    Units = Column(Integer, nullable=False)
    Description = Column(Text)
    IsActive = Column(Boolean, default=True)

    # Relationships
    class_schedules = relationship("ClassSchedule", back_populates="course")

class Attendance(Base):
    __tablename__ = "attendance"

    AttendanceID = Column(Integer, primary_key=True, index=True)
    StudentID = Column(Integer, ForeignKey('student.StudentID', ondelete='CASCADE'))
    ClassScheduleID = Column(Integer, ForeignKey('class_schedule.ClassScheduleID', ondelete='CASCADE'))
    Date = Column(Date, nullable=False)
    TimeIn = Column(Time)
    TimeOut = Column(Time)
    Status = Column(Enum('Present', 'Late', 'Absent', 'Excused'))
    Remarks = Column(Text)

    # Relationships
    student = relationship("Student", back_populates="attendance_records")
    class_schedule = relationship("ClassSchedule", back_populates="attendance_records")
