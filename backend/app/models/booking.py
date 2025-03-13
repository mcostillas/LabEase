from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, Text, Date, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class Booking(Base):
    __tablename__ = "booking"

    BookingID = Column(Integer, primary_key=True, index=True)
    UserID = Column(Integer, ForeignKey('user.UserID', ondelete='SET NULL'))
    LabID = Column(Integer, ForeignKey('laboratory.LabID', ondelete='SET NULL'))
    BookingDate = Column(Date, nullable=False)
    StartTime = Column(Time, nullable=False)
    EndTime = Column(Time, nullable=False)
    Status = Column(Enum('Pending', 'Reviewed', 'Approved', 'Rejected'), default='Pending')

    # Relationships
    user = relationship("User", back_populates="bookings")
    laboratory = relationship("Laboratory", back_populates="bookings")
    approval = relationship("BookingApproval", back_populates="booking", uselist=False)
    review = relationship("BookingReview", back_populates="booking", uselist=False)

class BookingApproval(Base):
    __tablename__ = "bookingapproval"

    ApprovalID = Column(Integer, primary_key=True, index=True)
    BookingID = Column(Integer, ForeignKey('booking.BookingID', ondelete='SET NULL'))
    ApproverID = Column(Integer, ForeignKey('user.UserID', ondelete='SET NULL'))
    ApprovalDate = Column(DateTime, server_default=func.now())
    Decision = Column(Enum('Approved', 'Rejected'), nullable=False)
    Reason = Column(Text)

    # Relationships
    booking = relationship("Booking", back_populates="approval")
    approver = relationship("User")

class BookingReview(Base):
    __tablename__ = "bookingreview"

    ReviewID = Column(Integer, primary_key=True, index=True)
    BookingID = Column(Integer, ForeignKey('booking.BookingID', ondelete='SET NULL'))
    ReviewerID = Column(Integer, ForeignKey('user.UserID', ondelete='SET NULL'))
    ReviewDate = Column(DateTime, server_default=func.now())
    Remarks = Column(Text)
    Status = Column(Enum('Pending', 'Reviewed', 'Rejected'), default='Pending')

    # Relationships
    booking = relationship("Booking", back_populates="review")
    reviewer = relationship("User")

class Schedule(Base):
    __tablename__ = "schedule"

    ScheduleID = Column(Integer, primary_key=True, index=True)
    LabID = Column(Integer, ForeignKey('laboratory.LabID', ondelete='CASCADE'))
    StartTime = Column(Time, nullable=False)
    EndTime = Column(Time, nullable=False)
    Date = Column(Date, nullable=False)
    ScheduleType = Column(Enum('Regular', 'Special'), nullable=False)

    # Relationship
    laboratory = relationship("Laboratory", back_populates="schedules")

class ClassSchedule(Base):
    __tablename__ = "class_schedule"

    ClassScheduleID = Column(Integer, primary_key=True, index=True)
    CourseID = Column(Integer, ForeignKey('course.CourseID', ondelete='SET NULL'))
    InstructorID = Column(Integer, ForeignKey('instructor.InstructorID', ondelete='SET NULL'))
    LabID = Column(Integer, ForeignKey('laboratory.LabID', ondelete='SET NULL'))
    DayOfWeek = Column(Enum('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'), nullable=False)
    StartTime = Column(Time, nullable=False)
    EndTime = Column(Time, nullable=False)
    Semester = Column(String(20), nullable=False)
    SchoolYear = Column(String(20), nullable=False)
    Section = Column(String(20), nullable=False)
    IsActive = Column(Integer, default=1)

    # Relationships
    course = relationship("Course", back_populates="class_schedules")
    instructor = relationship("Instructor", back_populates="class_schedules")
    laboratory = relationship("Laboratory", back_populates="class_schedules")
    attendance_records = relationship("Attendance", back_populates="class_schedule")
