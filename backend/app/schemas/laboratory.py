from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from enum import Enum

class EquipmentStatus(str, Enum):
    working = "Working"
    maintenance = "Maintenance"
    broken = "Broken"

class SoftwareStatus(str, Enum):
    active = "Active"
    expired = "Expired"
    maintenance = "Maintenance"

class InstallationStatus(str, Enum):
    installed = "Installed"
    pending = "Pending"
    failed = "Failed"

class MaintenanceStatus(str, Enum):
    pending = "Pending"
    in_progress = "InProgress"
    resolved = "Resolved"
    cancelled = "Cancelled"

class IncidentCategory(str, Enum):
    equipment = "Equipment"
    software = "Software"
    security = "Security"
    other = "Other"

class IncidentSeverity(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"
    critical = "Critical"

class IncidentStatus(str, Enum):
    open = "Open"
    in_progress = "InProgress"
    resolved = "Resolved"
    closed = "Closed"

# Laboratory Schemas
class LaboratoryBase(BaseModel):
    LabName: str
    Capacity: int

class LaboratoryCreate(LaboratoryBase):
    pass

class Laboratory(LaboratoryBase):
    LabID: int

    class Config:
        from_attributes = True

# Equipment Schemas
class LabEquipmentBase(BaseModel):
    Name: str
    Description: Optional[str] = None
    Status: EquipmentStatus = EquipmentStatus.working
    LastMaintenanceDate: Optional[date] = None
    NextMaintenanceDate: Optional[date] = None

class LabEquipmentCreate(LabEquipmentBase):
    LabID: int

class LabEquipment(LabEquipmentBase):
    EquipmentID: int
    LabID: int
    laboratory: Laboratory

    class Config:
        from_attributes = True

# Software Schemas
class LabSoftwareBase(BaseModel):
    Name: str
    Version: str
    LicenseKey: Optional[str] = None
    LicenseExpiry: Optional[date] = None
    Description: Optional[str] = None
    Status: SoftwareStatus = SoftwareStatus.active

class LabSoftwareCreate(LabSoftwareBase):
    pass

class LabSoftware(LabSoftwareBase):
    SoftwareID: int

    class Config:
        from_attributes = True

# Software Installation Schemas
class LabSoftwareInstallationBase(BaseModel):
    InstallationDate: date
    LastUpdateDate: Optional[date] = None
    Status: InstallationStatus = InstallationStatus.pending

class LabSoftwareInstallationCreate(LabSoftwareInstallationBase):
    SoftwareID: int
    LabID: int

class LabSoftwareInstallation(LabSoftwareInstallationBase):
    InstallationID: int
    SoftwareID: int
    LabID: int
    software: LabSoftware
    laboratory: Laboratory

    class Config:
        from_attributes = True

# Maintenance Log Schemas
class MaintenanceLogBase(BaseModel):
    IssueDescription: str
    Status: MaintenanceStatus = MaintenanceStatus.pending
    Resolution: Optional[str] = None

class MaintenanceLogCreate(MaintenanceLogBase):
    EquipmentID: int
    ReportedByID: int
    AssignedTechnicianID: Optional[int] = None

class MaintenanceLog(MaintenanceLogBase):
    LogID: int
    EquipmentID: int
    ReportedByID: int
    AssignedTechnicianID: Optional[int]
    ReportedAt: datetime
    ResolvedAt: Optional[datetime]
    equipment: LabEquipment

    class Config:
        from_attributes = True

# Incident Report Schemas
class IncidentReportBase(BaseModel):
    IncidentDate: datetime
    Category: IncidentCategory
    Description: str
    Severity: IncidentSeverity
    Status: IncidentStatus = IncidentStatus.open
    Resolution: Optional[str] = None

class IncidentReportCreate(IncidentReportBase):
    ReportedByID: int
    LabID: int
    EquipmentID: Optional[int] = None

class IncidentReport(IncidentReportBase):
    ReportID: int
    ReportedByID: int
    LabID: int
    EquipmentID: Optional[int]
    ResolvedByID: Optional[int]
    ResolvedAt: Optional[datetime]
    laboratory: Laboratory
    equipment: Optional[LabEquipment]

    class Config:
        from_attributes = True
