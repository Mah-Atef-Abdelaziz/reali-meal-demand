"""
Synthetic Data Generation Configuration
Defines all parameters for generating realistic meal demand data.
"""
import os
from datetime import date

# ============================================================
# GENERATION PARAMETERS
# ============================================================

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Date range: 2 years of historical data
START_DATE = date(2024, 1, 1)
END_DATE = date(2025, 12, 31)

# Employee generation
NUM_EMPLOYEES = 100_000
EMPLOYEE_AGE_RANGE = (22, 62)
EMPLOYEE_WEIGHT_RANGE = (55.0, 120.0)

# Grades (oil & gas industry style)
GRADES = ["G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10",
          "G11", "G12", "G13", "G14", "G15"]

# Shifts
SHIFTS = ["morning", "afternoon", "night", "rotational"]
SHIFT_WEIGHTS = [0.50, 0.25, 0.15, 0.10]

# Dietary preferences
DIETARY_PREFS = ["standard", "vegetarian", "halal_strict", "low_carb",
                 "high_protein", "diabetic_friendly"]
DIETARY_WEIGHTS = [0.60, 0.08, 0.15, 0.07, 0.06, 0.04]

# ============================================================
# DEPARTMENTS (matching schema.sql seed)
# ============================================================
DEPARTMENTS = [
    ("Engineering", "ENG"), ("Operations", "OPS"), ("Finance", "FIN"),
    ("Human Resources", "HR"), ("Information Technology", "IT"),
    ("Marketing", "MKT"), ("Sales", "SLS"), ("Legal", "LGL"),
    ("Research & Development", "R&D"), ("Quality Assurance", "QA"),
    ("Procurement", "PRC"), ("Logistics", "LOG"),
    ("Health & Safety", "HSE"), ("Administration", "ADM"),
    ("Maintenance", "MNT"), ("Drilling", "DRL"),
    ("Production", "PRD"), ("Geology", "GEO"),
    ("Environmental", "ENV"), ("Executive", "EXC"),
]

# Department size distribution (proportional)
DEPT_SIZE_WEIGHTS = [
    0.12, 0.15, 0.04, 0.03, 0.05, 0.03, 0.04, 0.02,
    0.06, 0.04, 0.03, 0.05, 0.04, 0.03, 0.08, 0.07,
    0.06, 0.03, 0.02, 0.01,
]

# ============================================================
# LOCATIONS (matching schema.sql seed)
# ============================================================
LOCATIONS = [
    ("Headquarters", "HQ-RYD", "office", "Riyadh", 2000),
    ("Jeddah Office", "OFF-JED", "office", "Jeddah", 800),
    ("Dammam Office", "OFF-DMM", "office", "Dammam", 600),
    ("Al Khobar Office", "OFF-KHB", "office", "Al Khobar", 400),
    ("Jubail Industrial", "ONS-JBL", "onshore", "Jubail", 1500),
    ("Yanbu Plant", "ONS-YNB", "onshore", "Yanbu", 1200),
    ("Ras Tanura Refinery", "ONS-RST", "onshore", "Ras Tanura", 1800),
    ("Abqaiq Processing", "ONS-ABQ", "onshore", "Abqaiq", 1000),
    ("Shaybah Field", "OFS-SHB", "offshore", "Shaybah", 600),
    ("Safaniyah Platform", "OFS-SFN", "offshore", "Safaniyah", 500),
    ("Zuluf Platform", "OFS-ZLF", "offshore", "Zuluf", 400),
    ("Marjan Platform", "OFS-MRJ", "offshore", "Marjan", 450),
    ("Berri Field", "OFS-BRI", "offshore", "Berri", 350),
    ("Khurais Plant", "ONS-KHR", "onshore", "Khurais", 900),
    ("KAUST Campus", "OFF-KST", "office", "Thuwal", 300),
]

# Location assignment weights (proportional to capacity)
LOCATION_WEIGHTS = [cap for _, _, _, _, cap in LOCATIONS]

# ============================================================
# MEAL CONFIGURATION
# ============================================================

# Base meal request rates by period (fraction of present employees)
BASE_MEAL_RATES = {
    "breakfast": 0.35,
    "lunch": 0.72,
    "dinner": 0.28,
}

# Day-of-week multipliers (Sun=0 in Saudi work week; Fri/Sat are weekend)
DOW_MULTIPLIERS = {
    0: 1.05,   # Sunday (first work day)
    1: 1.00,   # Monday
    2: 1.02,   # Tuesday
    3: 0.98,   # Wednesday
    4: 0.95,   # Thursday (last work day)
    5: 0.30,   # Friday (weekend — only offshore/essential)
    6: 0.35,   # Saturday (weekend — only offshore/essential)
}

# Location type multipliers for meal requests
LOCATION_TYPE_MEAL_MULT = {
    "office": 0.70,      # Office workers eat out more
    "onshore": 0.85,     # Plant workers mostly eat on-site
    "offshore": 0.95,    # Offshore has very high on-site eating
}

# Monthly seasonality (hot regions — summer reduces appetite)
MONTH_MULTIPLIERS = {
    1: 1.05, 2: 1.03, 3: 1.00, 4: 0.98, 5: 0.95, 6: 0.88,
    7: 0.85, 8: 0.85, 9: 0.90, 10: 0.95, 11: 1.00, 12: 1.08,
}

# Weather impact on hot meals
WEATHER_MEAL_IMPACT = {
    "sunny": 1.00,
    "cloudy": 1.02,
    "rainy": 1.08,    # People stay in, eat on-site
    "stormy": 1.12,
    "snowy": 1.10,
    "foggy": 1.03,
    "windy": 0.97,
}

# Attendance rate by location type
BASE_ATTENDANCE_RATE = {
    "office": 0.82,
    "onshore": 0.90,
    "offshore": 0.95,
}

# Hot meal waste rate (fraction of prepared that's wasted)
BASE_WASTE_RATE = 0.15  # 15% baseline waste

# ============================================================
# SAUDI ARABIA HOLIDAYS (2024-2025)
# ============================================================
HOLIDAYS = [
    # 2024
    (date(2024, 2, 22), "Founding Day", True),
    (date(2024, 3, 30), "Eid al-Fitr Start", True),
    (date(2024, 3, 31), "Eid al-Fitr", True),
    (date(2024, 4, 1), "Eid al-Fitr", True),
    (date(2024, 4, 2), "Eid al-Fitr End", True),
    (date(2024, 6, 7), "Arafat Day", True),
    (date(2024, 6, 8), "Eid al-Adha Start", True),
    (date(2024, 6, 9), "Eid al-Adha", True),
    (date(2024, 6, 10), "Eid al-Adha", True),
    (date(2024, 6, 11), "Eid al-Adha End", True),
    (date(2024, 7, 7), "Islamic New Year", True),
    (date(2024, 9, 15), "Saudi National Day", True),
    (date(2024, 9, 16), "Prophet Birthday", True),
    # 2025
    (date(2025, 2, 22), "Founding Day", True),
    (date(2025, 3, 19), "Eid al-Fitr Start", True),
    (date(2025, 3, 20), "Eid al-Fitr", True),
    (date(2025, 3, 21), "Eid al-Fitr", True),
    (date(2025, 3, 22), "Eid al-Fitr End", True),
    (date(2025, 5, 27), "Arafat Day", True),
    (date(2025, 5, 28), "Eid al-Adha Start", True),
    (date(2025, 5, 29), "Eid al-Adha", True),
    (date(2025, 5, 30), "Eid al-Adha", True),
    (date(2025, 5, 31), "Eid al-Adha End", True),
    (date(2025, 6, 26), "Islamic New Year", True),
    (date(2025, 9, 5), "Prophet Birthday", True),
    (date(2025, 9, 23), "Saudi National Day", True),
]

# ============================================================
# WEATHER PROFILES BY CITY
# ============================================================
WEATHER_PROFILES = {
    "Riyadh":     {"summer_high": 46, "summer_low": 30, "winter_high": 22, "winter_low": 8,  "rain_prob": 0.03},
    "Jeddah":     {"summer_high": 42, "summer_low": 28, "winter_high": 28, "winter_low": 18, "rain_prob": 0.05},
    "Dammam":     {"summer_high": 44, "summer_low": 28, "winter_high": 22, "winter_low": 10, "rain_prob": 0.04},
    "Al Khobar":  {"summer_high": 44, "summer_low": 28, "winter_high": 22, "winter_low": 10, "rain_prob": 0.04},
    "Jubail":     {"summer_high": 45, "summer_low": 29, "winter_high": 21, "winter_low": 9,  "rain_prob": 0.04},
    "Yanbu":      {"summer_high": 43, "summer_low": 27, "winter_high": 26, "winter_low": 16, "rain_prob": 0.03},
    "Ras Tanura": {"summer_high": 44, "summer_low": 29, "winter_high": 22, "winter_low": 11, "rain_prob": 0.03},
    "Abqaiq":     {"summer_high": 46, "summer_low": 30, "winter_high": 23, "winter_low": 9,  "rain_prob": 0.02},
    "Shaybah":    {"summer_high": 50, "summer_low": 32, "winter_high": 25, "winter_low": 10, "rain_prob": 0.01},
    "Safaniyah":  {"summer_high": 44, "summer_low": 28, "winter_high": 20, "winter_low": 8,  "rain_prob": 0.04},
    "Zuluf":      {"summer_high": 43, "summer_low": 27, "winter_high": 20, "winter_low": 9,  "rain_prob": 0.04},
    "Marjan":     {"summer_high": 43, "summer_low": 27, "winter_high": 20, "winter_low": 9,  "rain_prob": 0.04},
    "Berri":      {"summer_high": 44, "summer_low": 28, "winter_high": 21, "winter_low": 9,  "rain_prob": 0.03},
    "Khurais":    {"summer_high": 47, "summer_low": 31, "winter_high": 24, "winter_low": 9,  "rain_prob": 0.02},
    "Thuwal":     {"summer_high": 40, "summer_low": 27, "winter_high": 27, "winter_low": 17, "rain_prob": 0.05},
}

# Random seed for reproducibility
RANDOM_SEED = 42
