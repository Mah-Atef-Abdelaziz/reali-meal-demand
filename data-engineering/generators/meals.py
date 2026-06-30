"""
Attendance and meal transaction generator.
Generates ~2M+ meal transactions with realistic patterns.
"""
import numpy as np
import pandas as pd
from datetime import timedelta, date
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    START_DATE, END_DATE, LOCATIONS, RANDOM_SEED, OUTPUT_DIR,
    BASE_ATTENDANCE_RATE, BASE_MEAL_RATES, DOW_MULTIPLIERS,
    LOCATION_TYPE_MEAL_MULT, MONTH_MULTIPLIERS, WEATHER_MEAL_IMPACT,
    BASE_WASTE_RATE, HOLIDAYS
)

np.random.seed(RANDOM_SEED)

# Pre-compute holiday dates as a set
HOLIDAY_DATES = {h[0] for h in HOLIDAYS}


def _get_location_type(loc_id: int) -> str:
    """Get location type by ID (1-indexed)."""
    return LOCATIONS[loc_id - 1][2]


def generate_attendance_and_meals(employees_df: pd.DataFrame,
                                   weather_df: pd.DataFrame) -> tuple:
    """
    Generate attendance and meal transactions.
    Uses chunked processing to manage memory.
    """
    print("Generating attendance & meal transactions...")
    print("  This may take several minutes for 100K employees x 730 days...")

    days = (END_DATE - START_DATE).days + 1
    dates = [START_DATE + timedelta(days=d) for d in range(days)]

    # Pre-index weather data for fast lookup
    weather_lookup = {}
    for _, row in weather_df.iterrows():
        key = (int(row["location_id"]), row["weather_date"])
        weather_lookup[key] = row["condition"]

    # Only process a sample of active employees to prevent out-of-memory and speed up local execution
    active_emps = employees_df[employees_df["is_active"] == True].copy().head(2000)
    print(f"  Processing sampled {len(active_emps):,} active employees...")

    # Meal type IDs by period (matching schema seed data)
    meal_ids_by_period = {
        "breakfast": [9, 10, 11, 12, 18, 20],   # Ful, Shakshuka, Omelette, Pancakes, Fruit, Yogurt
        "lunch": [1, 2, 3, 4, 5, 7, 8, 17, 19], # Chicken, Biryani, Kebab, Mandi, Fish, Veg, Lentil, Salad, Sandwich
        "dinner": [6, 13, 14, 15, 16],           # Shrimp, Fish, Pasta, Shawarma, Mixed Grill
    }

    attendance_rows = []
    transaction_rows = []
    att_id = 1
    txn_id = 1

    # Process in monthly chunks to manage memory
    chunk_dates = {}
    for d in dates:
        key = (d.year, d.month)
        if key not in chunk_dates:
            chunk_dates[key] = []
        chunk_dates[key].append(d)

    for (year, month), month_dates in chunk_dates.items():
        month_mult = MONTH_MULTIPLIERS.get(month, 1.0)

        # Sample a subset of employees for each day (not all attend every day)
        for d in month_dates:
            date_str = d.strftime("%Y-%m-%d")
            dow = d.weekday()  # 0=Mon ... 6=Sun; convert to our scheme
            # Python weekday: Mon=0..Sun=6; Egypt: Sun=0 is first workday
            # Map: Sun(6)->0, Mon(0)->1, Tue(1)->2, Wed(2)->3, Thu(3)->4, Fri(4)->5, Sat(5)->6
            egypt_dow = (dow + 2) % 7
            dow_mult = DOW_MULTIPLIERS.get(egypt_dow, 1.0)
            is_holiday = d in HOLIDAY_DATES
            is_weekend = egypt_dow in (5, 6)

            # For each location, determine who attends
            for loc_id in range(1, len(LOCATIONS) + 1):
                loc_type = _get_location_type(loc_id)
                loc_emps = active_emps[active_emps["work_location_id"] == loc_id]
                if len(loc_emps) == 0:
                    continue

                # Base attendance rate
                att_rate = BASE_ATTENDANCE_RATE[loc_type]

                # Weekend / holiday adjustments
                if is_holiday:
                    att_rate *= 0.10 if loc_type == "office" else 0.50
                elif is_weekend:
                    att_rate *= 0.05 if loc_type == "office" else 0.60

                # Who is present? Bernoulli sampling
                present_mask = np.random.random(len(loc_emps)) < att_rate
                present_emps = loc_emps[present_mask]

                # Record attendance (sample to reduce output size — keep ~20% detail)
                if np.random.random() < 0.20:
                    for _, emp in present_emps.iterrows():
                        attendance_rows.append({
                            "id": att_id,
                            "employee_id": emp["id"],
                            "attendance_date": date_str,
                            "is_present": True,
                            "work_location_id": loc_id,
                        })
                        att_id += 1

                # Weather impact
                weather_key = (loc_id, date_str)
                weather_cond = weather_lookup.get(weather_key, "sunny")
                weather_mult = WEATHER_MEAL_IMPACT.get(weather_cond, 1.0)

                # Generate meal transactions for present employees
                for period in ["breakfast", "lunch", "dinner"]:
                    base_rate = BASE_MEAL_RATES[period]
                    loc_mult = LOCATION_TYPE_MEAL_MULT[loc_type]

                    final_rate = base_rate * dow_mult * month_mult * loc_mult * weather_mult
                    final_rate = min(final_rate, 0.98)  # Cap at 98%

                    # Which present employees request this meal?
                    meal_mask = np.random.random(len(present_emps)) < final_rate
                    meal_emps = present_emps[meal_mask]

                    # Assign meal types
                    available_meals = meal_ids_by_period[period]
                    if len(meal_emps) > 0:
                        chosen_meals = np.random.choice(available_meals, size=len(meal_emps))
                        # Waste: some meals go uneaten (prepared but wasted)
                        waste_mask = np.random.random(len(meal_emps)) < (BASE_WASTE_RATE * dow_mult)

                        for idx, (_, emp) in enumerate(meal_emps.iterrows()):
                            transaction_rows.append({
                                "id": txn_id,
                                "employee_id": emp["id"],
                                "transaction_date": date_str,
                                "period": period,
                                "meal_type_id": int(chosen_meals[idx]),
                                "location_id": loc_id,
                                "quantity": 1,
                                "was_wasted": bool(waste_mask[idx]),
                            })
                            txn_id += 1

        print(f"  Processed {year}-{month:02d}: {txn_id - 1:,} transactions so far...")

    # Save attendance
    att_df = pd.DataFrame(attendance_rows)
    att_path = os.path.join(OUTPUT_DIR, "attendance.csv")
    att_df.to_csv(att_path, index=False)
    print(f"  Saved {len(att_df):,} attendance records to {att_path}")

    # Save transactions
    txn_df = pd.DataFrame(transaction_rows)
    txn_path = os.path.join(OUTPUT_DIR, "meal_transactions.csv")
    txn_df.to_csv(txn_path, index=False)
    print(f"  Saved {len(txn_df):,} meal transactions to {txn_path}")

    return att_df, txn_df


if __name__ == "__main__":
    # Load prerequisite data
    emp_df = pd.read_csv(os.path.join(OUTPUT_DIR, "employees.csv"))
    weather_df = pd.read_csv(os.path.join(OUTPUT_DIR, "weather_data.csv"))
    generate_attendance_and_meals(emp_df, weather_df)
