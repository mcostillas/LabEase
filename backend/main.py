from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
from datetime import timedelta, datetime
from typing import Optional
import jwt

from database import engine, get_db
from models import Base, User, Instructor, Credentials

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Get the absolute path to the frontend directory
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))

# Mount the frontend directory
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT Configuration
SECRET_KEY = "your-secret-key"  # In production, use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.Email == email).first()
    if user is None:
        raise credentials_exception
    return user

@app.get("/")
async def read_root():
    return FileResponse(os.path.join(frontend_path, "landing_page.html"))

@app.post("/api/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Find user by email
    user = db.query(User).filter(User.Email == form_data.username).first()
    
    if not user or not user.credentials or not user.credentials.IsActive:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not user.credentials.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user.Email}
    )
    
    # Get additional user info if instructor
    instructor_info = None
    if user.UserType == "Instructor":
        instructor = db.query(Instructor).filter(Instructor.UserID == user.UserID).first()
        if instructor:
            instructor_info = {
                "department": instructor.Department,
                "position": instructor.Position,
                "specialization": instructor.Specialization
            }
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.UserType,
        "user_id": user.UserID,
        "full_name": user.FullName,
        "instructor_info": instructor_info
    }

@app.get("/api/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return {
        "email": current_user.Email,
        "full_name": current_user.FullName,
        "role": current_user.UserType
    }

@app.get("/api/instructor/profile")
async def get_instructor_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.UserType != "Instructor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not an instructor"
        )
    
    instructor = db.query(Instructor).filter(Instructor.UserID == current_user.UserID).first()
    if not instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instructor profile not found"
        )
    
    return {
        "instructor_id": instructor.InstructorID,
        "department": instructor.Department,
        "position": instructor.Position,
        "specialization": instructor.Specialization,
        "employee_id": instructor.EmployeeID
    }

# Test endpoint to verify the database connection
@app.get("/api/test-db")
async def test_db(db: Session = Depends(get_db)):
    try:
        # Get all users
        users = db.query(User).all()
        return {
            "status": "success",
            "user_count": len(users),
            "users": [
                {
                    "id": user.UserID,
                    "name": user.FullName,
                    "email": user.Email,
                    "type": user.UserType
                }
                for user in users
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@app.post("/api/setup-test-users")
async def setup_test_users(db: Session = Depends(get_db)):
    # Create test admin user
    admin = User(
        FirstName="Admin",
        LastName="User",
        Email="admin@labease.com",
        ContactNumber="1234567890",
        UserType="Admin"
    )
    admin_credentials = Credentials()
    admin_credentials.set_password("admin123")
    admin_credentials.IsActive = True
    admin.credentials = admin_credentials
    
    # Create test instructor user
    instructor = User(
        FirstName="Instructor",
        LastName="User",
        Email="instructor@labease.com",
        ContactNumber="0987654321",
        UserType="Instructor"
    )
    instructor_credentials = Credentials()
    instructor_credentials.set_password("instructor123")
    instructor_credentials.IsActive = True
    instructor.credentials = instructor_credentials
    
    db.add(admin)
    db.add(instructor)
    db.commit()
    
    return {"message": "Test users created successfully"}
