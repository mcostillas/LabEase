from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from enum import Enum

class CourseBase(BaseModel):
    CourseCode: str
    CourseName: str
    Department: str
    Units: int
    Description: Optional[str] = None
    IsActive: bool = True

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    CourseID: int

    class Config:
        from_attributes = True

# Response Models
class CourseWithSchedule(Course):
    class_schedules: List['ClassScheduleInfo']

class ClassScheduleInfo(BaseModel):
    ClassScheduleID: int
    InstructorName: str
    LabName: str
    DayOfWeek: str
    StartTime: str
    EndTime: str
    Section: str
    StudentCount: int

    class Config:
        from_attributes = True

class CourseStatistics(BaseModel):
    total_students: int
    attendance_rate: float
    lab_utilization: float
    equipment_usage: dict

# Request Models
class CourseFilter(BaseModel):
    department: Optional[str] = None
    semester: Optional[str] = None
    school_year: Optional[str] = None
    instructor_id: Optional[int] = None
    is_active: Optional[bool] = None

CourseWithSchedule.update_forward_refs()
