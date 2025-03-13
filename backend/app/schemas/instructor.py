from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date, time
from .laboratory import Laboratory, LabEquipment
from .schedule import ClassSchedule, Attendance
from .booking import Booking

class DashboardData(BaseModel):
    today_schedule: List[ClassSchedule]
    upcoming_classes: List[ClassSchedule]
    recent_activities: List[dict]  # Will contain mixed activity types
    equipment_status: List[dict]  # Equipment status for assigned labs

    class Config:
        from_attributes = True

class ActivityHistory(BaseModel):
    activity_id: int
    activity_type: str  # Class, LabUsage, Maintenance, Incident
    date: datetime
    description: str
    details: dict  # Will contain activity-specific details

    class Config:
        from_attributes = True

class AssignedLab(BaseModel):
    lab: Laboratory
    schedule: ClassSchedule
    equipment: List[LabEquipment]
    active_bookings: List[Booking]

    class Config:
        from_attributes = True

class StudentInfo(BaseModel):
    student_id: int
    full_name: str
    student_number: str
    course: str
    year_level: int
    attendance_records: List[Attendance]

    class Config:
        from_attributes = True

class IncidentReportCreate(BaseModel):
    lab_id: int
    equipment_id: Optional[int]
    incident_type: str
    description: str
    severity: str
    action_taken: Optional[str]

class IncidentReport(IncidentReportCreate):
    report_id: int
    reported_by: str
    reported_at: datetime
    status: str
    resolution: Optional[str]
    resolved_at: Optional[datetime]

    class Config:
        from_attributes = True

# Request Models
class ScheduleRequest(BaseModel):
    semester: Optional[str]
    school_year: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]

class AttendanceRecord(BaseModel):
    student_id: int
    status: str
    time_in: Optional[time]
    time_out: Optional[time]
    remarks: Optional[str]

class BulkAttendanceCreate(BaseModel):
    class_schedule_id: int
    date: date
    records: List[AttendanceRecord]

# Response Models
class InstructorDashboardResponse(BaseModel):
    instructor: dict
    dashboard_data: DashboardData
    notifications: List[dict]

class InstructorScheduleResponse(BaseModel):
    current_semester: str
    current_year: str
    schedules: List[ClassSchedule]
    total_hours: int
    total_classes: int

class InstructorHistoryResponse(BaseModel):
    activities: List[ActivityHistory]
    statistics: dict  # Summary statistics of activities
    total_records: int
