"""Pydantic Schemas — Request/Response models for all API endpoints."""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Any
from datetime import date, datetime
from enum import Enum


# ==================== AUTH ====================
class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    email: str
    password: str = Field(min_length=6)
    role: str = "viewer"

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    role: str
    username: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    is_active: bool
    last_login: Optional[datetime] = None
    class Config:
        from_attributes = True


# ==================== EMPLOYEES ====================
class EmployeeResponse(BaseModel):
    id: int
    employee_number: str
    first_name: str
    last_name: str
    email: Optional[str] = None
    department_id: int
    work_location_id: int
    grade: Optional[str] = None
    age: Optional[int] = None
    is_active: bool
    shift: Optional[str] = None
    dietary_preference: Optional[str] = None
    class Config:
        from_attributes = True

class EmployeeListResponse(BaseModel):
    items: List[EmployeeResponse]
    total: int
    page: int
    page_size: int


# ==================== MEALS ====================
class MealTypeResponse(BaseModel):
    id: int
    name: str
    category: str
    temperature: str
    period: str
    estimated_cost: float
    is_active: bool
    class Config:
        from_attributes = True


# ==================== PREDICTIONS ====================
class PredictionRequest(BaseModel):
    prediction_date: date
    location_id: Optional[int] = None  # None = all locations

class PredictionResponse(BaseModel):
    prediction_date: date
    location_id: int
    location_name: Optional[str] = None
    period: str
    predicted_count: int
    confidence_score: float
    recommended_quantity: int
    predicted_waste: int
    explanation: Optional[str] = None

class PredictionSummary(BaseModel):
    date: date
    total_breakfast: int
    total_lunch: int
    total_dinner: int
    total_predicted: int
    total_waste: int
    confidence: float
    predictions: List[PredictionResponse]


# ==================== CHATBOT ====================
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    data: Optional[Any] = None
    suggestions: Optional[List[str]] = None

class ChatHistoryResponse(BaseModel):
    session_id: str
    title: Optional[str] = None
    messages: List[dict]
    created_at: datetime


# ==================== DASHBOARD ====================
class KPIResponse(BaseModel):
    total_predicted_today: int = 0
    total_actual_today: int = 0
    waste_percentage: float = 0.0
    prediction_accuracy: float = 0.0
    cost_savings_monthly: float = 0.0
    carbon_footprint_reduction_kg: float = 0.0
    active_employees: int = 0
    locations_count: int = 0

class TrendDataPoint(BaseModel):
    date: date
    predicted: int
    actual: int
    waste: int

class DashboardResponse(BaseModel):
    kpis: KPIResponse
    trends: List[TrendDataPoint] = []
    top_locations: List[dict] = []
    department_breakdown: List[dict] = []
    meal_popularity: List[dict] = []


# ==================== REPORTS ====================
class ReportRequest(BaseModel):
    report_type: str = Field(description="daily, weekly, monthly, executive")
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    location_id: Optional[int] = None
    format: str = "pdf"  # pdf or excel

class ReportResponse(BaseModel):
    report_id: str
    report_type: str
    file_path: str
    generated_at: datetime


# ==================== RECOMMENDATIONS ====================
class RecommendationResponse(BaseModel):
    id: int
    category: str  # "quantity", "waste", "menu", "cost", "timing"
    title: str
    description: str
    impact: str  # "high", "medium", "low"
    metric_value: Optional[float] = None
    metric_unit: Optional[str] = None
    action: str
    generated_at: datetime


# ==================== COMMON ====================
class PaginationParams(BaseModel):
    page: int = 1
    page_size: int = 20
    sort_by: Optional[str] = None
    sort_order: str = "desc"

class MessageResponse(BaseModel):
    message: str
    success: bool = True

class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
