from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Optional
from .. import models, schemas
from ..database import get_db
from ..utils.auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_password_hash,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter()

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user account is active
    credentials = db.query(models.Credentials).filter(
        models.Credentials.UserID == user.UserID
    ).first()
    if credentials.AccountStatus != "Active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is not active"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.Email, "type": user.UserType},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_type": user.UserType
    }

@router.post("/register", response_model=schemas.User)
async def register_user(
    user_data: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    # Check if email already exists
    existing_user = db.query(models.User).filter(
        models.User.Email == user_data.Email
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    db_user = models.User(
        FullName=user_data.FullName,
        Email=user_data.Email,
        ContactNumber=user_data.ContactNumber,
        UserType=user_data.UserType
    )
    db.add(db_user)
    db.flush()  # Get UserID without committing
    
    # Create credentials
    db_credentials = models.Credentials(
        UserID=db_user.UserID,
        Password=get_password_hash(user_data.password),
        AccountStatus="Active"
    )
    db.add(db_credentials)
    
    # Create specific user type record
    if user_data.UserType == "Student":
        db_student = models.Student(
            UserID=db_user.UserID,
            StudentNumber=user_data.student.StudentNumber,
            Course=user_data.student.Course,
            YearLevel=user_data.student.YearLevel,
            Department=user_data.student.Department
        )
        db.add(db_student)
    elif user_data.UserType == "Instructor":
        db_instructor = models.Instructor(
            UserID=db_user.UserID,
            Department=user_data.instructor.Department,
            EmployeeID=user_data.instructor.EmployeeID,
            Position=user_data.instructor.Position,
            Specialization=user_data.instructor.Specialization
        )
        db.add(db_instructor)
    elif user_data.UserType == "Guest":
        db_guest = models.Guest(
            UserID=db_user.UserID,
            Organization=user_data.guest.Organization,
            Purpose=user_data.guest.Purpose,
            ValidIDType=user_data.guest.ValidIDType,
            ValidIDNumber=user_data.guest.ValidIDNumber
        )
        db.add(db_guest)
    
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/logout")
async def logout(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Log the logout event
    logout_log = models.LoginLogout(
        UserID=current_user.UserID,
        LogoutTime=datetime.utcnow(),
        LogDate=datetime.utcnow().date()
    )
    db.add(logout_log)
    db.commit()
    
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@router.post("/password-reset-request")
async def request_password_reset(
    email: str,
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.Email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Generate reset token
    reset_token = create_access_token(
        data={"sub": user.Email, "type": "reset"},
        expires_delta=timedelta(hours=1)
    )
    
    # Update user credentials with reset token
    credentials = db.query(models.Credentials).filter(
        models.Credentials.UserID == user.UserID
    ).first()
    credentials.ResetToken = reset_token
    credentials.ResetTokenExpiry = datetime.utcnow() + timedelta(hours=1)
    db.commit()
    
    # In a real application, send this token via email
    return {"message": "Password reset instructions sent to email"}

@router.post("/reset-password")
async def reset_password(
    token: str,
    new_password: str,
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid reset token"
            )
        
        user = db.query(models.User).filter(models.User.Email == email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        credentials = db.query(models.Credentials).filter(
            models.Credentials.UserID == user.UserID,
            models.Credentials.ResetToken == token,
            models.Credentials.ResetTokenExpiry > datetime.utcnow()
        ).first()
        
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )
        
        # Update password and clear reset token
        credentials.Password = get_password_hash(new_password)
        credentials.ResetToken = None
        credentials.ResetTokenExpiry = None
        db.commit()
        
        return {"message": "Password successfully reset"}
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid reset token"
        )
