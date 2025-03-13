from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, Boolean, Text, Date, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class Laboratory(Base):
    __tablename__ = "laboratory"

    LabID = Column(Integer, primary_key=True, index=True)
    LabName = Column(String(255), nullable=False)
    Capacity = Column(Integer, nullable=False)

    # Relationships
    equipment = relationship("LabEquipment", back_populates="laboratory")
    software_installations = relationship("LabSoftwareInstallation", back_populates="laboratory")
    bookings = relationship("Booking", back_populates="laboratory")
    schedules = relationship("Schedule", back_populates="laboratory")
    class_schedules = relationship("ClassSchedule", back_populates="laboratory")
    login_logs = relationship("LoginLogout", back_populates="laboratory")

class LabEquipment(Base):
    __tablename__ = "lab_equipment"

    EquipmentID = Column(Integer, primary_key=True, index=True)
    LabID = Column(Integer, ForeignKey('laboratory.LabID', ondelete='SET NULL'))
    Name = Column(String(255), nullable=False)
    Description = Column(Text)
    Status = Column(Enum('Working', 'Maintenance', 'Broken'), default='Working')
    LastMaintenanceDate = Column(Date)
    NextMaintenanceDate = Column(Date)

    # Relationships
    laboratory = relationship("Laboratory", back_populates="equipment")
    maintenance_logs = relationship("MaintenanceLog", back_populates="equipment")
    incident_reports = relationship("IncidentReport", back_populates="equipment")

class LabSoftware(Base):
    __tablename__ = "lab_software"

    SoftwareID = Column(Integer, primary_key=True, index=True)
    Name = Column(String(255), nullable=False)
    Version = Column(String(50), nullable=False)
    LicenseKey = Column(String(255))
    LicenseExpiry = Column(Date)
    Description = Column(Text)
    Status = Column(Enum('Active', 'Expired', 'Maintenance'), default='Active')

    # Relationships
    installations = relationship("LabSoftwareInstallation", back_populates="software")

class LabSoftwareInstallation(Base):
    __tablename__ = "lab_software_installation"

    InstallationID = Column(Integer, primary_key=True, index=True)
    SoftwareID = Column(Integer, ForeignKey('lab_software.SoftwareID', ondelete='CASCADE'))
    LabID = Column(Integer, ForeignKey('laboratory.LabID', ondelete='CASCADE'))
    InstallationDate = Column(Date, nullable=False)
    LastUpdateDate = Column(Date)
    Status = Column(Enum('Installed', 'Pending', 'Failed'), default='Pending')

    # Relationships
    software = relationship("LabSoftware", back_populates="installations")
    laboratory = relationship("Laboratory", back_populates="software_installations")

class MaintenanceLog(Base):
    __tablename__ = "maintenance_log"

    LogID = Column(Integer, primary_key=True, index=True)
    EquipmentID = Column(Integer, ForeignKey('lab_equipment.EquipmentID', ondelete='SET NULL'))
    ReportedByID = Column(Integer, ForeignKey('user.UserID', ondelete='SET NULL'))
    AssignedTechnicianID = Column(Integer, ForeignKey('user.UserID', ondelete='SET NULL'))
    IssueDescription = Column(Text, nullable=False)
    Status = Column(Enum('Pending', 'InProgress', 'Resolved', 'Cancelled'), default='Pending')
    Resolution = Column(Text)
    ReportedAt = Column(DateTime, server_default=func.now())
    ResolvedAt = Column(DateTime)

    # Relationships
    equipment = relationship("LabEquipment", back_populates="maintenance_logs")
    reported_by = relationship("User", foreign_keys=[ReportedByID])
    assigned_technician = relationship("User", foreign_keys=[AssignedTechnicianID])

class IncidentReport(Base):
    __tablename__ = "incident_reports"

    ReportID = Column(Integer, primary_key=True, index=True)
    ReportedByID = Column(Integer, ForeignKey('user.UserID', ondelete='SET NULL'))
    LabID = Column(Integer, ForeignKey('laboratory.LabID', ondelete='SET NULL'))
    EquipmentID = Column(Integer, ForeignKey('lab_equipment.EquipmentID', ondelete='SET NULL'))
    IncidentDate = Column(DateTime, nullable=False)
    Category = Column(Enum('Equipment', 'Software', 'Security', 'Other'), nullable=False)
    Description = Column(Text, nullable=False)
    Severity = Column(Enum('Low', 'Medium', 'High', 'Critical'), nullable=False)
    Status = Column(Enum('Open', 'InProgress', 'Resolved', 'Closed'), default='Open')
    Resolution = Column(Text)
    ResolvedByID = Column(Integer, ForeignKey('user.UserID', ondelete='SET NULL'))
    ResolvedAt = Column(DateTime)

    # Relationships
    reported_by = relationship("User", foreign_keys=[ReportedByID])
    resolved_by = relationship("User", foreign_keys=[ResolvedByID])
    laboratory = relationship("Laboratory", back_populates="incident_reports")
    equipment = relationship("LabEquipment", back_populates="incident_reports")
