from .user import User, Credentials, Student, Instructor, Guest, Admin
from .laboratory import Laboratory, LabEquipment, LabSoftware, LabSoftwareInstallation, MaintenanceLog, IncidentReport
from .booking import Booking, BookingApproval, BookingReview, Schedule, ClassSchedule
from .course import Course, Attendance

# Import all models here so they can be imported from models directly
__all__ = [
    'User', 'Credentials', 'Student', 'Instructor', 'Guest', 'Admin',
    'Laboratory', 'LabEquipment', 'LabSoftware', 'LabSoftwareInstallation',
    'MaintenanceLog', 'IncidentReport',
    'Booking', 'BookingApproval', 'BookingReview', 'Schedule', 'ClassSchedule',
    'Course', 'Attendance'
]
