"""SQLAlchemy ORM Models — All database tables."""
from sqlalchemy import (
    Column, Integer, BigInteger, String, Boolean, Date, DateTime, Time,
    ForeignKey, Text, Numeric, Enum, JSON, UniqueConstraint, Index, CheckConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum


# ==================== ENUMS ====================
class UserRole(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    kitchen_staff = "kitchen_staff"
    viewer = "viewer"

class MealPeriod(str, enum.Enum):
    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"

class LocationType(str, enum.Enum):
    office = "office"
    field = "field"
    industrial = "industrial"

class ShiftType(str, enum.Enum):
    morning = "morning"
    afternoon = "afternoon"
    night = "night"
    rotational = "rotational"


# ==================== CORE MODELS ====================

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    code = Column(String(10), unique=True, nullable=False)
    head_name = Column(String(150))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    employees = relationship("Employee", back_populates="department")


class WorkLocation(Base):
    __tablename__ = "work_locations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    location_type = Column(String(20), nullable=False)
    city = Column(String(100))
    country = Column(String(100), default="Egypt")
    capacity = Column(Integer, default=500)
    is_active = Column(Boolean, default=True)
    latitude = Column(Numeric(10, 7))
    longitude = Column(Numeric(10, 7))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    employees = relationship("Employee", back_populates="work_location")


class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    employee_number = Column(String(20), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(200), unique=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    work_location_id = Column(Integer, ForeignKey("work_locations.id"), nullable=False)
    grade = Column(String(10))
    age = Column(Integer)
    weight = Column(Numeric(5, 2))
    hire_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)
    shift = Column(String(20), default="morning")
    dietary_preference = Column(String(50), default="standard")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    department = relationship("Department", back_populates="employees")
    work_location = relationship("WorkLocation", back_populates="employees")


# ==================== MEAL MODELS ====================

class MealType(Base):
    __tablename__ = "meal_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    temperature = Column(String(10), default="hot")
    period = Column(String(20), nullable=False)
    estimated_cost = Column(Numeric(8, 2), default=0)
    preparation_time_minutes = Column(Integer, default=60)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class DailyMenu(Base):
    __tablename__ = "daily_menus"
    id = Column(Integer, primary_key=True, index=True)
    menu_date = Column(Date, nullable=False)
    location_id = Column(Integer, ForeignKey("work_locations.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("employees.id"))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    __table_args__ = (UniqueConstraint("menu_date", "location_id"),)
    items = relationship("MenuItem", back_populates="menu", cascade="all, delete-orphan")


class MenuItem(Base):
    __tablename__ = "menu_items"
    id = Column(Integer, primary_key=True, index=True)
    menu_id = Column(Integer, ForeignKey("daily_menus.id", ondelete="CASCADE"), nullable=False)
    meal_type_id = Column(Integer, ForeignKey("meal_types.id"), nullable=False)
    planned_quantity = Column(Integer, default=0)
    actual_prepared = Column(Integer, default=0)
    price = Column(Numeric(8, 2), default=0)
    menu = relationship("DailyMenu", back_populates="items")


# ==================== OPERATIONAL MODELS ====================

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    attendance_date = Column(Date, nullable=False)
    is_present = Column(Boolean, default=False)
    check_in = Column(DateTime(timezone=True))
    check_out = Column(DateTime(timezone=True))
    work_location_id = Column(Integer, ForeignKey("work_locations.id"))
    __table_args__ = (UniqueConstraint("employee_id", "attendance_date"),)


class MealTransaction(Base):
    __tablename__ = "meal_transactions"
    id = Column(BigInteger, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    transaction_date = Column(Date, nullable=False)
    period = Column(String(20), nullable=False)
    meal_type_id = Column(Integer, ForeignKey("meal_types.id"))
    location_id = Column(Integer, ForeignKey("work_locations.id"), nullable=False)
    quantity = Column(Integer, default=1)
    was_wasted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ==================== EXTERNAL DATA ====================

class WeatherData(Base):
    __tablename__ = "weather_data"
    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey("work_locations.id"), nullable=False)
    weather_date = Column(Date, nullable=False)
    temperature_high = Column(Numeric(5, 2))
    temperature_low = Column(Numeric(5, 2))
    temperature_avg = Column(Numeric(5, 2))
    humidity_percent = Column(Integer)
    condition = Column(String(20), default="sunny")
    wind_speed_kmh = Column(Numeric(5, 2))
    precipitation_mm = Column(Numeric(5, 2), default=0)


class HolidayCalendar(Base):
    __tablename__ = "holiday_calendar"
    id = Column(Integer, primary_key=True, index=True)
    holiday_date = Column(Date, nullable=False)
    name = Column(String(200), nullable=False)
    is_national = Column(Boolean, default=True)
    is_company = Column(Boolean, default=False)
    affects_locations = Column(Text, default="all")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CompanyEvent(Base):
    __tablename__ = "company_events"
    id = Column(Integer, primary_key=True, index=True)
    event_date = Column(Date, nullable=False)
    name = Column(String(200), nullable=False)
    event_type = Column(String(50), default="other")
    location_id = Column(Integer, ForeignKey("work_locations.id"))
    expected_attendees = Column(Integer, default=0)
    affects_meals = Column(Boolean, default=True)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Visitor(Base):
    __tablename__ = "visitors"
    id = Column(Integer, primary_key=True, index=True)
    visit_date = Column(Date, nullable=False)
    location_id = Column(Integer, ForeignKey("work_locations.id"), nullable=False)
    visitor_count = Column(Integer, default=1)
    company_name = Column(String(200))
    purpose = Column(String(200))
    meals_requested = Column(Boolean, default=True)
    meal_periods = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ==================== AI MODELS ====================

class PredictionResult(Base):
    __tablename__ = "prediction_results"
    id = Column(BigInteger, primary_key=True, index=True)
    prediction_date = Column(Date, nullable=False)
    location_id = Column(Integer, ForeignKey("work_locations.id"), nullable=False)
    period = Column(String(20), nullable=False)
    predicted_count = Column(Integer, nullable=False)
    actual_count = Column(Integer)
    confidence_score = Column(Numeric(5, 4))
    recommended_quantity = Column(Integer)
    predicted_waste = Column(Integer, default=0)
    actual_waste = Column(Integer)
    model_version = Column(String(50))
    features_used = Column(JSON)
    shap_explanation = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ModelLog(Base):
    __tablename__ = "model_logs"
    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(100), nullable=False)
    model_version = Column(String(50), nullable=False)
    algorithm = Column(String(50), nullable=False)
    training_date = Column(DateTime(timezone=True), server_default=func.now())
    mae = Column(Numeric(10, 4))
    rmse = Column(Numeric(10, 4))
    mape = Column(Numeric(10, 4))
    r2_score = Column(Numeric(10, 6))
    hyperparameters = Column(JSON)
    feature_importance = Column(JSON)
    training_duration_seconds = Column(Integer)
    dataset_size = Column(Integer)
    is_active = Column(Boolean, default=False)
    notes = Column(Text)


# ==================== SYSTEM MODELS ====================

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    role = Column(String(20), default="viewer")
    employee_id = Column(Integer, ForeignKey("employees.id"))
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    chat_sessions = relationship("ChatSession", back_populates="user")


class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    prediction_id = Column(BigInteger, ForeignKey("prediction_results.id"))
    rating = Column(String(1))
    comment = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ChatSession(Base):
    __tablename__ = "chat_sessions"
    id = Column(String(36), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    user = relationship("User", back_populates="chat_sessions")
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    session_id = Column(String(36), ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    metadata_ = Column("metadata", JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    session = relationship("ChatSession", back_populates="messages")


class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String(100), nullable=False)
    resource_type = Column(String(100))
    resource_id = Column(String(100))
    details = Column(JSON)
    ip_address = Column(String(45))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    notification_type = Column(String(30), nullable=False)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    data = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
