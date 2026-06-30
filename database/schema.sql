-- ============================================================
-- AI Meal Demand Prediction System — Complete Database Schema
-- PostgreSQL 16 | Normalized (3NF)
-- ============================================================

-- ==================== EXTENSIONS ====================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ==================== ENUM TYPES ====================
CREATE TYPE user_role AS ENUM ('admin', 'manager', 'kitchen_staff', 'viewer');
CREATE TYPE meal_period AS ENUM ('breakfast', 'lunch', 'dinner');
CREATE TYPE meal_temp AS ENUM ('hot', 'cold');
CREATE TYPE location_type AS ENUM ('office', 'field', 'industrial');
CREATE TYPE shift_type AS ENUM ('morning', 'afternoon', 'night', 'rotational');
CREATE TYPE weather_condition AS ENUM ('sunny', 'cloudy', 'rainy', 'stormy', 'snowy', 'foggy', 'windy');
CREATE TYPE event_type AS ENUM ('company_meeting', 'training', 'celebration', 'maintenance', 'external_visit', 'other');
CREATE TYPE notification_type AS ENUM ('prediction', 'waste_alert', 'recommendation', 'system', 'report');
CREATE TYPE feedback_rating AS ENUM ('1', '2', '3', '4', '5');

-- ==================== CORE TABLES ====================

-- Departments
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    code VARCHAR(10) NOT NULL UNIQUE,
    head_name VARCHAR(150),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Work Locations
CREATE TABLE work_locations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    code VARCHAR(20) NOT NULL UNIQUE,
    location_type location_type NOT NULL,
    city VARCHAR(100),
    country VARCHAR(100) DEFAULT 'Egypt',
    capacity INTEGER NOT NULL DEFAULT 500,
    is_active BOOLEAN DEFAULT TRUE,
    latitude DECIMAL(10, 7),
    longitude DECIMAL(10, 7),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Employees
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    employee_number VARCHAR(20) NOT NULL UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(200) UNIQUE,
    department_id INTEGER NOT NULL REFERENCES departments(id),
    work_location_id INTEGER NOT NULL REFERENCES work_locations(id),
    grade VARCHAR(10),
    age INTEGER CHECK (age >= 18 AND age <= 70),
    weight DECIMAL(5, 2) CHECK (weight > 30 AND weight < 300),
    hire_date DATE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    shift shift_type DEFAULT 'morning',
    dietary_preference VARCHAR(50) DEFAULT 'standard',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_employees_department ON employees(department_id);
CREATE INDEX idx_employees_location ON employees(work_location_id);
CREATE INDEX idx_employees_active ON employees(is_active);

-- ==================== MEAL TABLES ====================

-- Meal Types
CREATE TABLE meal_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL, -- e.g., 'chicken', 'beef', 'fish', 'vegetarian'
    temperature meal_temp NOT NULL DEFAULT 'hot',
    period meal_period NOT NULL,
    estimated_cost DECIMAL(8, 2) DEFAULT 0,
    preparation_time_minutes INTEGER DEFAULT 60,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Daily Menu
CREATE TABLE daily_menus (
    id SERIAL PRIMARY KEY,
    menu_date DATE NOT NULL,
    location_id INTEGER NOT NULL REFERENCES work_locations(id),
    created_by INTEGER REFERENCES employees(id),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(menu_date, location_id)
);

CREATE INDEX idx_daily_menus_date ON daily_menus(menu_date);

-- Menu Items (junction: daily_menus <-> meal_types)
CREATE TABLE menu_items (
    id SERIAL PRIMARY KEY,
    menu_id INTEGER NOT NULL REFERENCES daily_menus(id) ON DELETE CASCADE,
    meal_type_id INTEGER NOT NULL REFERENCES meal_types(id),
    planned_quantity INTEGER NOT NULL DEFAULT 0,
    actual_prepared INTEGER DEFAULT 0,
    price DECIMAL(8, 2) DEFAULT 0,
    UNIQUE(menu_id, meal_type_id)
);

-- ==================== OPERATIONAL TABLES ====================

-- Employee Eligibility
CREATE TABLE employee_eligibility (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL REFERENCES employees(id),
    period meal_period NOT NULL,
    is_eligible BOOLEAN DEFAULT TRUE,
    effective_from DATE NOT NULL,
    effective_to DATE,
    reason VARCHAR(200),
    UNIQUE(employee_id, period, effective_from)
);

-- Employee Schedule
CREATE TABLE employee_schedules (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL REFERENCES employees(id),
    schedule_date DATE NOT NULL,
    shift shift_type NOT NULL,
    is_working BOOLEAN DEFAULT TRUE,
    check_in_time TIME,
    check_out_time TIME,
    UNIQUE(employee_id, schedule_date)
);

CREATE INDEX idx_schedules_date ON employee_schedules(schedule_date);
CREATE INDEX idx_schedules_employee ON employee_schedules(employee_id);

-- Attendance
CREATE TABLE attendance (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL REFERENCES employees(id),
    attendance_date DATE NOT NULL,
    is_present BOOLEAN DEFAULT FALSE,
    check_in TIMESTAMP WITH TIME ZONE,
    check_out TIMESTAMP WITH TIME ZONE,
    work_location_id INTEGER REFERENCES work_locations(id),
    UNIQUE(employee_id, attendance_date)
);

CREATE INDEX idx_attendance_date ON attendance(attendance_date);
CREATE INDEX idx_attendance_employee ON attendance(employee_id);

-- Meal Transactions
CREATE TABLE meal_transactions (
    id BIGSERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL REFERENCES employees(id),
    transaction_date DATE NOT NULL,
    period meal_period NOT NULL,
    meal_type_id INTEGER REFERENCES meal_types(id),
    location_id INTEGER NOT NULL REFERENCES work_locations(id),
    quantity INTEGER DEFAULT 1,
    was_wasted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_transactions_date ON meal_transactions(transaction_date);
CREATE INDEX idx_transactions_employee ON meal_transactions(employee_id);
CREATE INDEX idx_transactions_period ON meal_transactions(period);
CREATE INDEX idx_transactions_location ON meal_transactions(location_id);
CREATE INDEX idx_transactions_date_period ON meal_transactions(transaction_date, period);

-- ==================== EXTERNAL DATA TABLES ====================

-- Weather Data
CREATE TABLE weather_data (
    id SERIAL PRIMARY KEY,
    location_id INTEGER NOT NULL REFERENCES work_locations(id),
    weather_date DATE NOT NULL,
    temperature_high DECIMAL(5, 2),
    temperature_low DECIMAL(5, 2),
    temperature_avg DECIMAL(5, 2),
    humidity_percent INTEGER,
    condition weather_condition DEFAULT 'sunny',
    wind_speed_kmh DECIMAL(5, 2),
    precipitation_mm DECIMAL(5, 2) DEFAULT 0,
    UNIQUE(location_id, weather_date)
);

CREATE INDEX idx_weather_date ON weather_data(weather_date);

-- Holiday Calendar
CREATE TABLE holiday_calendar (
    id SERIAL PRIMARY KEY,
    holiday_date DATE NOT NULL,
    name VARCHAR(200) NOT NULL,
    is_national BOOLEAN DEFAULT TRUE,
    is_company BOOLEAN DEFAULT FALSE,
    affects_locations TEXT DEFAULT 'all', -- 'all' or comma-separated location IDs
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(holiday_date, name)
);

CREATE INDEX idx_holidays_date ON holiday_calendar(holiday_date);

-- Company Events
CREATE TABLE company_events (
    id SERIAL PRIMARY KEY,
    event_date DATE NOT NULL,
    name VARCHAR(200) NOT NULL,
    event_type event_type DEFAULT 'other',
    location_id INTEGER REFERENCES work_locations(id),
    expected_attendees INTEGER DEFAULT 0,
    affects_meals BOOLEAN DEFAULT TRUE,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_events_date ON company_events(event_date);

-- Visitors
CREATE TABLE visitors (
    id SERIAL PRIMARY KEY,
    visit_date DATE NOT NULL,
    location_id INTEGER NOT NULL REFERENCES work_locations(id),
    visitor_count INTEGER NOT NULL DEFAULT 1,
    company_name VARCHAR(200),
    purpose VARCHAR(200),
    meals_requested BOOLEAN DEFAULT TRUE,
    meal_periods TEXT, -- comma-separated: 'breakfast,lunch'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_visitors_date ON visitors(visit_date);

-- ==================== AI TABLES ====================

-- Prediction Results
CREATE TABLE prediction_results (
    id BIGSERIAL PRIMARY KEY,
    prediction_date DATE NOT NULL,
    location_id INTEGER NOT NULL REFERENCES work_locations(id),
    period meal_period NOT NULL,
    predicted_count INTEGER NOT NULL,
    actual_count INTEGER,
    confidence_score DECIMAL(5, 4),
    recommended_quantity INTEGER,
    predicted_waste INTEGER DEFAULT 0,
    actual_waste INTEGER,
    model_version VARCHAR(50),
    features_used JSONB,
    shap_explanation JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(prediction_date, location_id, period)
);

CREATE INDEX idx_predictions_date ON prediction_results(prediction_date);

-- Model Logs
CREATE TABLE model_logs (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL,
    model_version VARCHAR(50) NOT NULL,
    algorithm VARCHAR(50) NOT NULL,
    training_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    mae DECIMAL(10, 4),
    rmse DECIMAL(10, 4),
    mape DECIMAL(10, 4),
    r2_score DECIMAL(10, 6),
    hyperparameters JSONB,
    feature_importance JSONB,
    training_duration_seconds INTEGER,
    dataset_size INTEGER,
    is_active BOOLEAN DEFAULT FALSE,
    notes TEXT
);

-- ==================== SYSTEM TABLES ====================

-- Users (authentication)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(200) NOT NULL UNIQUE,
    password_hash VARCHAR(256) NOT NULL,
    role user_role NOT NULL DEFAULT 'viewer',
    employee_id INTEGER REFERENCES employees(id),
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Feedback
CREATE TABLE feedback (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    prediction_id BIGINT REFERENCES prediction_results(id),
    rating feedback_rating,
    comment TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Chat History
CREATE TABLE chat_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id INTEGER NOT NULL REFERENCES users(id),
    title VARCHAR(200),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE chat_messages (
    id BIGSERIAL PRIMARY KEY,
    session_id UUID NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_chat_messages_session ON chat_messages(session_id);

-- Audit Logs
CREATE TABLE audit_logs (
    id BIGSERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(100),
    resource_id VARCHAR(100),
    details JSONB,
    ip_address INET,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_audit_logs_user ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_created ON audit_logs(created_at);

-- Notifications
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    notification_type notification_type NOT NULL,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_notifications_user ON notifications(user_id);
CREATE INDEX idx_notifications_unread ON notifications(user_id, is_read) WHERE is_read = FALSE;

-- ==================== SEED DATA ====================

-- Default departments
INSERT INTO departments (name, code) VALUES
('Engineering', 'ENG'),
('Operations', 'OPS'),
('Finance', 'FIN'),
('Human Resources', 'HR'),
('Information Technology', 'IT'),
('Marketing', 'MKT'),
('Sales', 'SLS'),
('Legal', 'LGL'),
('Research & Development', 'R&D'),
('Quality Assurance', 'QA'),
('Procurement', 'PRC'),
('Logistics', 'LOG'),
('Health & Safety', 'HSE'),
('Administration', 'ADM'),
('Maintenance', 'MNT'),
('Drilling', 'DRL'),
('Production', 'PRD'),
('Geology', 'GEO'),
('Environmental', 'ENV'),
('Executive', 'EXC');

-- Default work locations
INSERT INTO work_locations (name, code, location_type, city, capacity) VALUES
('Headquarters', 'HQ-CAI', 'office', 'Cairo', 2000),
('Alexandria Office', 'OFF-ALX', 'office', 'Alexandria', 800),
('Suez Office', 'OFF-SUZ', 'office', 'Suez', 600),
('6th October Office', 'OFF-OCT', 'office', '6th October City', 400),
('Ain Sokhna Industrial', 'IND-ASK', 'industrial', 'Ain Sokhna', 1500),
('Borg El-Arab Plant', 'IND-BRG', 'industrial', 'Borg El-Arab', 1200),
('El-Hamra Refinery', 'IND-HMR', 'industrial', 'El-Alamein', 1800),
('Abu Qir Processing', 'IND-ABQ', 'industrial', 'Abu Qir', 1000),
('Ras Gharib Field', 'FLD-RSG', 'field', 'Ras Gharib', 600),
('Gulf of Suez Platform', 'FLD-GOS', 'field', 'Gulf of Suez', 500),
('Western Desert Field', 'FLD-WDS', 'field', 'Western Desert', 400),
('Belayim Platform', 'FLD-BLY', 'field', 'Belayim', 450),
('Assiut Refinery', 'IND-AST', 'industrial', 'Assiut', 350),
('El-Mex Industrial', 'IND-MEX', 'industrial', 'El-Mex', 900),
('New Administrative Capital', 'OFF-NAC', 'office', 'New Capital', 300);

-- Default meal types
INSERT INTO meal_types (name, category, temperature, period, estimated_cost, preparation_time_minutes) VALUES
('Grilled Chicken', 'chicken', 'hot', 'lunch', 15.00, 45),
('Chicken Biryani', 'chicken', 'hot', 'lunch', 12.00, 60),
('Beef Kebab', 'beef', 'hot', 'lunch', 18.00, 40),
('Lamb Mandi', 'beef', 'hot', 'lunch', 22.00, 90),
('Fish Fillet', 'fish', 'hot', 'lunch', 16.00, 30),
('Shrimp Curry', 'fish', 'hot', 'dinner', 20.00, 45),
('Vegetable Stew', 'vegetarian', 'hot', 'lunch', 10.00, 40),
('Lentil Soup', 'vegetarian', 'hot', 'lunch', 8.00, 30),
('Ful Medames', 'vegetarian', 'hot', 'breakfast', 6.00, 20),
('Shakshuka', 'egg', 'hot', 'breakfast', 8.00, 25),
('Omelette Station', 'egg', 'hot', 'breakfast', 7.00, 15),
('Pancakes', 'pastry', 'hot', 'breakfast', 5.00, 20),
('Grilled Fish', 'fish', 'hot', 'dinner', 17.00, 35),
('Pasta Bolognese', 'pasta', 'hot', 'dinner', 11.00, 30),
('Chicken Shawarma', 'chicken', 'hot', 'dinner', 13.00, 25),
('Mixed Grill', 'beef', 'hot', 'dinner', 25.00, 50),
('Salad Bowl', 'vegetarian', 'cold', 'lunch', 7.00, 10),
('Fruit Platter', 'vegetarian', 'cold', 'breakfast', 5.00, 10),
('Sandwich Platter', 'mixed', 'cold', 'lunch', 9.00, 15),
('Yogurt Parfait', 'dairy', 'cold', 'breakfast', 4.00, 5);

-- Default admin user (password: admin123 — change in production!)
INSERT INTO users (username, email, password_hash, role) VALUES
('admin', 'admin@reali.com', crypt('admin123', gen_salt('bf')), 'admin');
