from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db
from .routers import auth, users, labs, bookings, schedules, equipment, instructors
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create all database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LabEase API",
    description="Backend API for the LabEase Laboratory Management System",
    version="1.0.0"
)

# Get CORS origins from environment variables
CORS_ORIGINS = eval(os.getenv("CORS_ORIGINS", '["http://localhost:5173", "http://localhost:3000"]'))

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(labs.router, prefix="/api/labs", tags=["Laboratories"])
app.include_router(bookings.router, prefix="/api/bookings", tags=["Bookings"])
app.include_router(schedules.router, prefix="/api/schedules", tags=["Schedules"])
app.include_router(equipment.router, prefix="/api/equipment", tags=["Equipment"])
app.include_router(instructors.router, prefix="/api/instructors", tags=["Instructors"])

@app.get("/")
def read_root():
    return {"message": "Welcome to LabEase API"}
