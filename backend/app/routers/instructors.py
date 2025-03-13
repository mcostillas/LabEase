from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date, time, timedelta
from .. import models, schemas
from ..database import get_db
from ..utils.auth import get_current_user, check_instructor_role

router = APIRouter()

@router.get("/dashboard", response_model=schemas.instructor.InstructorDashboardResponse)
async def get_instructor_dashboard(
    current_user: models.User = Depends(check_instructor_role),
    db: Session = Depends(get_db)
):
    # Get instructor details
    instructor = db.query(models.Instructor).filter(
        models.Instructor.UserID == current_user.UserID
    ).first()
    
    if not instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instructor profile not found"
        )
    
    # Get today's date
    today = datetime.now().date()
    
    # Get today's schedule
    today_schedule = db.query(models.ClassSchedule).filter(
        models.ClassSchedule.InstructorID == instructor.InstructorID,
        models.ClassSchedule.DayOfWeek == today.strftime("%A"),
        models.ClassSchedule.IsActive == True
    ).all()
    
    # Get upcoming classes (next 7 days)
    next_week = today + timedelta(days=7)
    upcoming_classes = db.query(models.ClassSchedule).filter(
        models.ClassSchedule.InstructorID == instructor.InstructorID,
        models.ClassSchedule.IsActive == True
    ).all()
    
    # Get recent lab activities
    recent_activities = []
    
    # Get lab bookings
    recent_bookings = db.query(models.Booking).join(
        models.Laboratory
    ).filter(
        models.Laboratory.LabInChargeID == instructor.InstructorID,
        models.Booking.BookingDate >= today - timedelta(days=7)
    ).all()
    
    for booking in recent_bookings:
        recent_activities.append({
            "type": "booking",
            "date": booking.BookingDate,
            "details": f"Lab booking by {booking.user.FullName}"
        })
    
    # Get maintenance logs
    recent_maintenance = db.query(models.MaintenanceLog).join(
        models.LabEquipment
    ).join(
        models.Laboratory
    ).filter(
        models.Laboratory.LabInChargeID == instructor.InstructorID,
        models.MaintenanceLog.ReportedAt >= datetime.now() - timedelta(days=7)
    ).all()
    
    for maintenance in recent_maintenance:
        recent_activities.append({
            "type": "maintenance",
            "date": maintenance.ReportedAt,
            "details": f"Equipment maintenance: {maintenance.equipment.Name}"
        })
    
    # Get equipment status for assigned labs
    equipment_status = []
    assigned_labs = db.query(models.Laboratory).filter(
        models.Laboratory.LabInChargeID == instructor.InstructorID
    ).all()
    
    for lab in assigned_labs:
        equipment = db.query(models.LabEquipment).filter(
            models.LabEquipment.LabID == lab.LabID
        ).all()
        
        for item in equipment:
            equipment_status.append({
                "lab_name": lab.LabName,
                "equipment_name": item.Name,
                "status": item.Status,
                "needs_maintenance": item.NextMaintenanceDate and item.NextMaintenanceDate <= today
            })
    
    # Get recent notifications
    notifications = db.query(models.Notification).filter(
        models.Notification.UserID == current_user.UserID,
        models.Notification.IsRead == False
    ).order_by(models.Notification.CreatedAt.desc()).limit(5).all()
    
    return schemas.instructor.InstructorDashboardResponse(
        instructor={
            "id": instructor.InstructorID,
            "name": current_user.FullName,
            "department": instructor.Department,
            "position": instructor.Position
        },
        dashboard_data=schemas.instructor.DashboardData(
            today_schedule=today_schedule,
            upcoming_classes=upcoming_classes,
            recent_activities=recent_activities,
            equipment_status=equipment_status
        ),
        notifications=[{
            "id": n.NotificationID,
            "message": n.Message,
            "created_at": n.CreatedAt,
            "type": n.NotificationType
        } for n in notifications]
    )

@router.get("/schedule", response_model=schemas.instructor.InstructorScheduleResponse)
async def get_instructor_schedule(
    semester: Optional[str] = None,
    school_year: Optional[str] = None,
    current_user: models.User = Depends(check_instructor_role),
    db: Session = Depends(get_db)
):
    instructor = db.query(models.Instructor).filter(
        models.Instructor.UserID == current_user.UserID
    ).first()
    
    if not instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instructor profile not found"
        )
    
    # If semester and school year not provided, get current ones
    if not semester or not school_year:
        current_schedule = db.query(models.ClassSchedule).filter(
            models.ClassSchedule.InstructorID == instructor.InstructorID,
            models.ClassSchedule.IsActive == True
        ).first()
        
        if current_schedule:
            semester = current_schedule.Semester
            school_year = current_schedule.SchoolYear
    
    # Get all schedules for the semester
    schedules = db.query(models.ClassSchedule).filter(
        models.ClassSchedule.InstructorID == instructor.InstructorID,
        models.ClassSchedule.Semester == semester,
        models.ClassSchedule.SchoolYear == school_year
    ).all()
    
    # Calculate statistics
    total_hours = sum(
        (datetime.combine(date.today(), s.EndTime) - 
         datetime.combine(date.today(), s.StartTime)).seconds / 3600
        for s in schedules
    )
    
    return schemas.instructor.InstructorScheduleResponse(
        current_semester=semester,
        current_year=school_year,
        schedules=schedules,
        total_hours=total_hours,
        total_classes=len(schedules)
    )

@router.get("/history", response_model=schemas.instructor.InstructorHistoryResponse)
async def get_instructor_history(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    activity_type: Optional[str] = None,
    current_user: models.User = Depends(check_instructor_role),
    db: Session = Depends(get_db)
):
    instructor = db.query(models.Instructor).filter(
        models.Instructor.UserID == current_user.UserID
    ).first()
    
    if not instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instructor profile not found"
        )
    
    # Default to last 30 days if dates not provided
    if not start_date:
        start_date = datetime.now().date() - timedelta(days=30)
    if not end_date:
        end_date = datetime.now().date()
    
    activities = []
    
    # Get class sessions
    class_sessions = db.query(models.ClassSchedule).filter(
        models.ClassSchedule.InstructorID == instructor.InstructorID,
        models.ClassSchedule.IsActive == True
    ).all()
    
    for session in class_sessions:
        activities.append(schemas.instructor.ActivityHistory(
            activity_id=session.ClassScheduleID,
            activity_type="class",
            date=datetime.combine(start_date, session.StartTime),
            description=f"Class session: {session.Section}",
            details={
                "course": session.course.CourseName,
                "section": session.Section,
                "time": f"{session.StartTime.strftime('%H:%M')} - {session.EndTime.strftime('%H:%M')}"
            }
        ))
    
    # Get lab usage history
    lab_usage = db.query(models.Booking).join(
        models.Laboratory
    ).filter(
        models.Laboratory.LabInChargeID == instructor.InstructorID,
        models.Booking.BookingDate.between(start_date, end_date)
    ).all()
    
    for usage in lab_usage:
        activities.append(schemas.instructor.ActivityHistory(
            activity_id=usage.BookingID,
            activity_type="lab_usage",
            date=datetime.combine(usage.BookingDate, usage.StartTime),
            description=f"Lab usage: {usage.laboratory.LabName}",
            details={
                "lab": usage.laboratory.LabName,
                "user": usage.user.FullName,
                "purpose": usage.Purpose
            }
        ))
    
    # Filter by activity type if specified
    if activity_type:
        activities = [a for a in activities if a.activity_type == activity_type]
    
    # Calculate statistics
    statistics = {
        "total_classes": len([a for a in activities if a.activity_type == "class"]),
        "total_lab_usage": len([a for a in activities if a.activity_type == "lab_usage"]),
        "total_hours": sum(
            (datetime.combine(date.today(), s.EndTime) - 
             datetime.combine(date.today(), s.StartTime)).seconds / 3600
            for s in class_sessions
        )
    }
    
    return schemas.instructor.InstructorHistoryResponse(
        activities=activities,
        statistics=statistics,
        total_records=len(activities)
    )

@router.post("/attendance", response_model=List[schemas.schedule.Attendance])
async def record_class_attendance(
    attendance_data: schemas.instructor.BulkAttendanceCreate,
    current_user: models.User = Depends(check_instructor_role),
    db: Session = Depends(get_db)
):
    instructor = db.query(models.Instructor).filter(
        models.Instructor.UserID == current_user.UserID
    ).first()
    
    # Verify class schedule belongs to instructor
    schedule = db.query(models.ClassSchedule).filter(
        models.ClassSchedule.ClassScheduleID == attendance_data.class_schedule_id,
        models.ClassSchedule.InstructorID == instructor.InstructorID
    ).first()
    
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class schedule not found or not authorized"
        )
    
    attendance_records = []
    for record in attendance_data.records:
        # Verify student is enrolled in the class
        student = db.query(models.Student).filter(
            models.Student.StudentID == record.student_id
        ).first()
        
        if not student:
            continue
        
        attendance = models.Attendance(
            StudentID=student.StudentID,
            ClassScheduleID=schedule.ClassScheduleID,
            Date=attendance_data.date,
            TimeIn=record.time_in,
            TimeOut=record.time_out,
            Status=record.status,
            Remarks=record.remarks
        )
        db.add(attendance)
        attendance_records.append(attendance)
    
    db.commit()
    for record in attendance_records:
        db.refresh(record)
    
    return attendance_records

@router.get("/labs", response_model=List[schemas.instructor.AssignedLab])
async def get_assigned_labs(
    current_user: models.User = Depends(check_instructor_role),
    db: Session = Depends(get_db)
):
    instructor = db.query(models.Instructor).filter(
        models.Instructor.UserID == current_user.UserID
    ).first()
    
    if not instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instructor profile not found"
        )
    
    assigned_labs = db.query(models.Laboratory).filter(
        models.Laboratory.LabInChargeID == instructor.InstructorID
    ).all()
    
    return assigned_labs

@router.post("/incidents", response_model=schemas.instructor.IncidentReport)
async def report_lab_incident(
    incident: schemas.instructor.IncidentReportCreate,
    current_user: models.User = Depends(check_instructor_role),
    db: Session = Depends(get_db)
):
    instructor = db.query(models.Instructor).filter(
        models.Instructor.UserID == current_user.UserID
    ).first()
    
    if not instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instructor profile not found"
        )
    
    incident_report = models.IncidentReport(
        InstructorID=instructor.InstructorID,
        IncidentDate=incident.incident_date,
        IncidentTime=incident.incident_time,
        Description=incident.description,
        LabID=incident.lab_id
    )
    db.add(incident_report)
    db.commit()
    db.refresh(incident_report)
    
    return incident_report

@router.get("/students", response_model=List[schemas.instructor.StudentInfo])
async def get_students_in_class(
    class_schedule_id: int,
    current_user: models.User = Depends(check_instructor_role),
    db: Session = Depends(get_db)
):
    instructor = db.query(models.Instructor).filter(
        models.Instructor.UserID == current_user.UserID
    ).first()
    
    if not instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instructor profile not found"
        )
    
    # Verify class schedule belongs to instructor
    schedule = db.query(models.ClassSchedule).filter(
        models.ClassSchedule.ClassScheduleID == class_schedule_id,
        models.ClassSchedule.InstructorID == instructor.InstructorID
    ).first()
    
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class schedule not found or not authorized"
        )
    
    students = db.query(models.Student).join(
        models.Enrollment
    ).filter(
        models.Enrollment.ClassScheduleID == class_schedule_id
    ).all()
    
    return students
