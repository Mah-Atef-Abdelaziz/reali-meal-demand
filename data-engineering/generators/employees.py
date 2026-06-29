"""Employee data generator — 100,000 realistic employee records."""
import numpy as np
import pandas as pd
from faker import Faker
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    NUM_EMPLOYEES, DEPARTMENTS, DEPT_SIZE_WEIGHTS, LOCATIONS,
    LOCATION_WEIGHTS, GRADES, SHIFTS, SHIFT_WEIGHTS,
    EMPLOYEE_AGE_RANGE, EMPLOYEE_WEIGHT_RANGE,
    DIETARY_PREFS, DIETARY_WEIGHTS, RANDOM_SEED, OUTPUT_DIR, START_DATE
)

fake = Faker(["ar_SA", "en_US"])
Faker.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


def generate_employees() -> pd.DataFrame:
    """Generate NUM_EMPLOYEES realistic employee records."""
    print(f"Generating {NUM_EMPLOYEES:,} employees...")

    total_cap = sum(LOCATION_WEIGHTS)
    loc_probs = [w / total_cap for w in LOCATION_WEIGHTS]

    total_dept = sum(DEPT_SIZE_WEIGHTS)
    dept_probs = [w / total_dept for w in DEPT_SIZE_WEIGHTS]

    # Pre-generate arrays for speed
    n = NUM_EMPLOYEES
    dept_ids = np.random.choice(range(1, len(DEPARTMENTS) + 1), size=n, p=dept_probs)
    loc_ids = np.random.choice(range(1, len(LOCATIONS) + 1), size=n, p=loc_probs)
    ages = np.random.randint(EMPLOYEE_AGE_RANGE[0], EMPLOYEE_AGE_RANGE[1] + 1, size=n)
    weights = np.round(np.random.normal(78, 15, size=n).clip(
        EMPLOYEE_WEIGHT_RANGE[0], EMPLOYEE_WEIGHT_RANGE[1]), 1)
    grades = np.random.choice(GRADES, size=n,
                               p=[0.03, 0.05, 0.08, 0.10, 0.12, 0.14, 0.13,
                                  0.11, 0.09, 0.06, 0.04, 0.02, 0.01, 0.01, 0.01])
    shifts = np.random.choice(SHIFTS, size=n, p=SHIFT_WEIGHTS)
    dietary = np.random.choice(DIETARY_PREFS, size=n, p=DIETARY_WEIGHTS)

    # Generate hire dates (spread over 15 years)
    hire_offsets = np.random.exponential(scale=1500, size=n).astype(int).clip(0, 5475)
    hire_dates = pd.to_datetime(START_DATE) - pd.to_timedelta(hire_offsets, unit="D")

    # Active status (95% active)
    is_active = np.random.choice([True, False], size=n, p=[0.95, 0.05])

    # Generate names in batches for speed
    first_names = []
    last_names = []
    for i in range(n):
        if i % 2 == 0:
            first_names.append(fake.first_name_male())
            last_names.append(fake.last_name())
        else:
            first_names.append(fake.first_name_female())
            last_names.append(fake.last_name())
        if (i + 1) % 25000 == 0:
            print(f"  Names generated: {i + 1:,}/{n:,}")

    # Employee numbers
    emp_numbers = [f"EMP{str(i + 1).zfill(6)}" for i in range(n)]

    # Emails
    emails = [f"{emp_numbers[i].lower()}@reali.com" for i in range(n)]

    df = pd.DataFrame({
        "id": range(1, n + 1),
        "employee_number": emp_numbers,
        "first_name": first_names,
        "last_name": last_names,
        "email": emails,
        "department_id": dept_ids,
        "work_location_id": loc_ids,
        "grade": grades,
        "age": ages,
        "weight": weights,
        "hire_date": hire_dates.strftime("%Y-%m-%d"),
        "is_active": is_active,
        "shift": shifts,
        "dietary_preference": dietary,
    })

    output_path = os.path.join(OUTPUT_DIR, "employees.csv")
    df.to_csv(output_path, index=False)
    print(f"  Saved {len(df):,} employees to {output_path}")
    return df


if __name__ == "__main__":
    generate_employees()
