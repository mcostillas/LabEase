from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date, time
from enum import Enum

class BookingStatus(str, Enum):
    pending = "Pending"
    reviewed = "Reviewed"
    approved = "Approved"
    rejected = "Rejected"

class ApprovalDecision(str, Enum):
    approved = "Approved"
    rejected = "Rejected"

class ReviewStatus(str, Enum):
    pending = "Pending"
    reviewed = "Reviewed"
    rejected = "Rejected"

# Booking Schemas
class BookingBase(BaseModel):
    BookingDate: date
    StartTime: time
    EndTime: time
    Status: BookingStatus = BookingStatus.pending

class BookingCreate(BookingBase):
    UserID: int
    LabID: int

class Booking(BookingBase):
    BookingID: int
    UserID: int
    LabID: int

    class Config:
        from_attributes = True

# Booking Approval Schemas
class BookingApprovalBase(BaseModel):
    Decision: ApprovalDecision
    Reason: Optional[str] = None

class BookingApprovalCreate(BookingApprovalBase):
    BookingID: int
    ApproverID: int

class BookingApproval(BookingApprovalBase):
    ApprovalID: int
    BookingID: int
    ApproverID: int
    ApprovalDate: datetime

    class Config:
        from_attributes = True

# Booking Review Schemas
class BookingReviewBase(BaseModel):
    Remarks: Optional[str] = None
    Status: ReviewStatus = ReviewStatus.pending

class BookingReviewCreate(BookingReviewBase):
    BookingID: int
    ReviewerID: int

class BookingReview(BookingReviewBase):
    ReviewID: int
    BookingID: int
    ReviewerID: int
    ReviewDate: datetime

    class Config:
        from_attributes = True

# Response Schemas
class BookingResponse(Booking):
    approval: Optional[BookingApproval]
    review: Optional[BookingReview]

class BookingListResponse(BaseModel):
    total: int
    items: List[BookingResponse]

# Request Schemas
class BookingFilter(BaseModel):
    status: Optional[BookingStatus] = None
    lab_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    user_id: Optional[int] = None
