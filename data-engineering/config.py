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

# Grades (industrial / corporate style)
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
# LOCATIONS — EGYPT (matching schema.sql seed)
# ============================================================
LOCATIONS = [
    ("Headquarters", "HQ-CAI", "office", "Cairo", 2000),
    ("Alexandria Office", "OFF-ALX", "office", "Alexandria", 800),
    ("Suez Office", "OFF-SUZ", "office", "Suez", 600),
    ("6th October Office", "OFF-OCT", "office", "6th October City", 400),
    ("Ain Sokhna Industrial", "IND-ASK", "industrial", "Ain Sokhna", 1500),
    ("Borg El-Arab Plant", "IND-BRG", "industrial", "Borg El-Arab", 1200),
    ("El-Hamra Refinery", "IND-HMR", "industrial", "El-Alamein", 1800),
    ("Abu Qir Processing", "IND-ABQ", "industrial", "Abu Qir", 1000),
    ("Ras Gharib Field", "FLD-RSG", "field", "Ras Gharib", 600),
    ("Gulf of Suez Platform", "FLD-GOS", "field", "Gulf of Suez", 500),
    ("Western Desert Field", "FLD-WDS", "field", "Western Desert", 400),
    ("Belayim Platform", "FLD-BLY", "field", "Belayim", 450),
    ("Assiut Refinery", "IND-AST", "industrial", "Assiut", 350),
    ("El-Mex Industrial", "IND-MEX", "industrial", "El-Mex", 900),
    ("New Administrative Capital", "OFF-NAC", "office", "New Capital", 300),
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

# Day-of-week multipliers (Sun=0 in Egypt work week; Fri/Sat are weekend)
DOW_MULTIPLIERS = {
    0: 1.05,   # Sunday (first work day)
    1: 1.00,   # Monday
    2: 1.02,   # Tuesday
    3: 0.98,   # Wednesday
    4: 0.95,   # Thursday (last work day)
    5: 0.30,   # Friday (weekend — only field/essential)
    6: 0.35,   # Saturday (weekend — only field/essential)
}

# Location type multipliers for meal requests
LOCATION_TYPE_MEAL_MULT = {
    "office": 0.70,        # Office workers eat out more
    "industrial": 0.85,    # Plant workers mostly eat on-site
    "field": 0.95,         # Field sites have very high on-site eating
}

# Monthly seasonality (hot climate — summer reduces appetite)
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
    "industrial": 0.90,
    "field": 0.95,
}

# Hot meal waste rate (fraction of prepared that's wasted)
BASE_WASTE_RATE = 0.15  # 15% baseline waste

# ============================================================
# EGYPT HOLIDAYS (2024-2025)
# ============================================================
HOLIDAYS = [
    # 2024
    (date(2024, 1, 7), "Coptic Christmas", True),
    (date(2024, 1, 25), "January 25 Revolution Day", True),
    (date(2024, 3, 30), "Eid al-Fitr Start", True),
    (date(2024, 3, 31), "Eid al-Fitr", True),
    (date(2024, 4, 1), "Eid al-Fitr", True),
    (date(2024, 4, 2), "Eid al-Fitr End", True),
    (date(2024, 4, 25), "Sinai Liberation Day", True),
    (date(2024, 5, 1), "Labour Day", True),
    (date(2024, 5, 6), "Sham El-Nessim", True),
    (date(2024, 6, 7), "Arafat Day", True),
    (date(2024, 6, 8), "Eid al-Adha Start", True),
    (date(2024, 6, 9), "Eid al-Adha", True),
    (date(2024, 6, 10), "Eid al-Adha", True),
    (date(2024, 6, 11), "Eid al-Adha End", True),
    (date(2024, 6, 30), "June 30 Revolution Day", True),
    (date(2024, 7, 7), "Islamic New Year", True),
    (date(2024, 7, 23), "July 23 Revolution Day", True),
    (date(2024, 9, 16), "Prophet Birthday", True),
    (date(2024, 10, 6), "Armed Forces Day (6th October)", True),
    # 2025
    (date(2025, 1, 7), "Coptic Christmas", True),
    (date(2025, 1, 25), "January 25 Revolution Day", True),
    (date(2025, 3, 19), "Eid al-Fitr Start", True),
    (date(2025, 3, 20), "Eid al-Fitr", True),
    (date(2025, 3, 21), "Eid al-Fitr", True),
    (date(2025, 3, 22), "Eid al-Fitr End", True),
    (date(2025, 4, 21), "Sham El-Nessim", True),
    (date(2025, 4, 25), "Sinai Liberation Day", True),
    (date(2025, 5, 1), "Labour Day", True),
    (date(2025, 5, 27), "Arafat Day", True),
    (date(2025, 5, 28), "Eid al-Adha Start", True),
    (date(2025, 5, 29), "Eid al-Adha", True),
    (date(2025, 5, 30), "Eid al-Adha", True),
    (date(2025, 5, 31), "Eid al-Adha End", True),
    (date(2025, 6, 26), "Islamic New Year", True),
    (date(2025, 6, 30), "June 30 Revolution Day", True),
    (date(2025, 7, 23), "July 23 Revolution Day", True),
    (date(2025, 9, 5), "Prophet Birthday", True),
    (date(2025, 10, 6), "Armed Forces Day (6th October)", True),
]

# ============================================================
# WEATHER PROFILES BY CITY — EGYPT
# ============================================================
WEATHER_PROFILES = {
    "Cairo":            {"summer_high": 38, "summer_low": 24, "winter_high": 20, "winter_low": 9,  "rain_prob": 0.05},
    "Alexandria":       {"summer_high": 32, "summer_low": 23, "winter_high": 18, "winter_low": 10, "rain_prob": 0.15},
    "Suez":             {"summer_high": 38, "summer_low": 24, "winter_high": 20, "winter_low": 10, "rain_prob": 0.04},
    "6th October City": {"summer_high": 38, "summer_low": 23, "winter_high": 19, "winter_low": 8,  "rain_prob": 0.05},
    "Ain Sokhna":       {"summer_high": 37, "summer_low": 25, "winter_high": 22, "winter_low": 12, "rain_prob": 0.03},
    "Borg El-Arab":     {"summer_high": 31, "summer_low": 22, "winter_high": 18, "winter_low": 9,  "rain_prob": 0.14},
    "El-Alamein":       {"summer_high": 32, "summer_low": 22, "winter_high": 18, "winter_low": 9,  "rain_prob": 0.12},
    "Abu Qir":          {"summer_high": 32, "summer_low": 23, "winter_high": 18, "winter_low": 10, "rain_prob": 0.13},
    "Ras Gharib":       {"summer_high": 40, "summer_low": 26, "winter_high": 22, "winter_low": 12, "rain_prob": 0.02},
    "Gulf of Suez":     {"summer_high": 38, "summer_low": 25, "winter_high": 21, "winter_low": 11, "rain_prob": 0.03},
    "Western Desert":   {"summer_high": 42, "summer_low": 25, "winter_high": 22, "winter_low": 8,  "rain_prob": 0.01},
    "Belayim":          {"summer_high": 39, "summer_low": 25, "winter_high": 21, "winter_low": 11, "rain_prob": 0.02},
    "Assiut":           {"summer_high": 40, "summer_low": 24, "winter_high": 21, "winter_low": 6,  "rain_prob": 0.02},
    "El-Mex":           {"summer_high": 32, "summer_low": 23, "winter_high": 18, "winter_low": 10, "rain_prob": 0.13},
    "New Capital":      {"summer_high": 38, "summer_low": 24, "winter_high": 20, "winter_low": 9,  "rain_prob": 0.05},
}

# Random seed for reproducibility
RANDOM_SEED = 42
