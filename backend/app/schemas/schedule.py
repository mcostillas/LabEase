from pydantic import BaseModel
from typing import Optional, List
from datetime import date, time
from enum import Enum

class DayOfWeek(str, Enum):
    monday = "Monday"
    tuesday = "Tuesday"
    wednesday = "Wednesday"
    thursday = "Thursday"
    friday = "Friday"
    saturday = "Saturday"
    sunday = "Sunday"

class ScheduleType(str, Enum):
    regular = "Regular"
    special = "Special"

class AttendanceStatus(str, Enum):
    present = "Present"
    late = "Late"
    absent = "Absent"
    excused = "Excused"

# Schedule Schemas
class ScheduleBase(BaseModel):
    StartTime: time
    EndTime: time
    Date: date
    ScheduleType: ScheduleType

class ScheduleCreate(ScheduleBase):
    LabID: int

class Schedule(ScheduleBase):
    ScheduleID: int
    LabID: int

    class Config:
        from_attributes = True

# Class Schedule Schemas
class ClassScheduleBase(BaseModel):
    DayOfWeek: DayOfWeek
    StartTime: time
    EndTime: time
    Semester: str
    SchoolYear: str
    Section: str
    IsActive: bool = True

class ClassScheduleCreate(ClassScheduleBase):
    CourseID: int
    InstructorID: int
    LabID: int

class ClassSchedule(ClassScheduleBase):
    ClassScheduleID: int
    CourseID: int
    InstructorID: int
    LabID: int

    class Config:
        from_attributes = True

# Attendance Schemas
class AttendanceBase(BaseModel):
    Date: date
    TimeIn: Optional[time] = None
    TimeOut: Optional[time] = None
    Status: AttendanceStatus
    Remarks: Optional[str] = None

class AttendanceCreate(AttendanceBase):
    StudentID: int
    ClassScheduleID: int

class Attendance(AttendanceBase):
    AttendanceID: int
    StudentID: int
    ClassScheduleID: int

    class Config:
        from_attributes = True

# Response Schemas
class ClassScheduleWithAttendance(ClassSchedule):
    attendance_records: List[Attendance]

class ScheduleResponse(BaseModel):
    regular_schedules: List[ClassSchedule]
    special_schedules: List[Schedule]

# Request Schemas
class ScheduleFilter(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    instructor_id: Optional[int] = None
    lab_id: Optional[int] = None
    semester: Optional[str] = None
    school_year: Optional[str] = None
