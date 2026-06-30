"""Visitors and company events generator."""
import numpy as np
import pandas as pd
from datetime import timedelta
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    START_DATE, END_DATE, LOCATIONS, RANDOM_SEED, OUTPUT_DIR, HOLIDAYS
)

np.random.seed(RANDOM_SEED + 3)

EVENT_TYPES = ["company_meeting", "training", "celebration", "maintenance", "external_visit", "other"]
EVENT_NAMES = {
    "company_meeting": ["Quarterly Review", "Board Meeting", "Town Hall", "Safety Meeting", "Budget Review"],
    "training": ["Safety Training", "Leadership Workshop", "Technical Certification", "Onboarding", "First Aid"],
    "celebration": ["Annual Day", "Eid Celebration", "National Day Event", "Team Building", "Awards Ceremony"],
    "maintenance": ["Turnaround", "Shutdown Maintenance", "Equipment Inspection", "Safety Drill"],
    "external_visit": ["Client Visit", "Auditor Visit", "Government Inspection", "Partner Meeting"],
    "other": ["Health Checkup", "Blood Donation Drive", "Career Fair", "Innovation Day"],
}
VISITOR_COMPANIES = [
    "Orascom Construction", "Ezz Steel", "ENPPI", "EGAS", "Sidi Kerir Petrochemicals",
    "El Sewedy Electric", "Arabian Cement", "Petrojet", "Eni Egypt",
    "KPMG", "Deloitte", "EY", "PwC", "McKinsey",
    "Ministry of Petroleum", "NTRA", "GAFI",
]


def generate_events() -> pd.DataFrame:
    """Generate company events over 2 years."""
    print("Generating company events...")
    days = (END_DATE - START_DATE).days + 1
    rows = []
    row_id = 1

    for day_offset in range(days):
        d = START_DATE + timedelta(days=day_offset)
        dow = d.weekday()
        if dow in (4, 5):  # Fri/Sat weekend — skip most events
            if np.random.random() > 0.02:
                continue

        # ~3% chance of event on any workday
        if np.random.random() < 0.03:
            etype = np.random.choice(EVENT_TYPES, p=[0.25, 0.20, 0.15, 0.15, 0.15, 0.10])
            ename = np.random.choice(EVENT_NAMES[etype])
            loc_id = np.random.randint(1, len(LOCATIONS) + 1)
            attendees = int(np.random.exponential(80)) + 10

            rows.append({
                "id": row_id,
                "event_date": d.strftime("%Y-%m-%d"),
                "name": ename,
                "event_type": etype,
                "location_id": loc_id,
                "expected_attendees": attendees,
                "affects_meals": etype != "maintenance",
                "notes": None,
            })
            row_id += 1

    df = pd.DataFrame(rows)
    output_path = os.path.join(OUTPUT_DIR, "company_events.csv")
    df.to_csv(output_path, index=False)
    print(f"  Saved {len(df):,} events to {output_path}")
    return df


def generate_visitors() -> pd.DataFrame:
    """Generate visitor records."""
    print("Generating visitor records...")
    days = (END_DATE - START_DATE).days + 1
    rows = []
    row_id = 1

    for day_offset in range(days):
        d = START_DATE + timedelta(days=day_offset)
        dow = d.weekday()
        if dow in (4, 5):
            continue

        # ~15% of workdays have visitors at any given location
        for loc_id in range(1, len(LOCATIONS) + 1):
            loc_type = LOCATIONS[loc_id - 1][2]
            # Office locations get more visitors
            visit_prob = 0.20 if loc_type == "office" else 0.08 if loc_type == "industrial" else 0.03
            if np.random.random() < visit_prob:
                count = int(np.random.exponential(5)) + 1
                company = np.random.choice(VISITOR_COMPANIES)
                purposes = ["Business Meeting", "Audit", "Site Visit", "Training", "Contract Discussion"]
                periods = np.random.choice(["breakfast,lunch", "lunch", "lunch,dinner", "breakfast,lunch,dinner"],
                                           p=[0.10, 0.50, 0.25, 0.15])
                rows.append({
                    "id": row_id,
                    "visit_date": d.strftime("%Y-%m-%d"),
                    "location_id": loc_id,
                    "visitor_count": count,
                    "company_name": company,
                    "purpose": np.random.choice(purposes),
                    "meals_requested": True,
                    "meal_periods": periods,
                })
                row_id += 1

    df = pd.DataFrame(rows)
    output_path = os.path.join(OUTPUT_DIR, "visitors.csv")
    df.to_csv(output_path, index=False)
    print(f"  Saved {len(df):,} visitor records to {output_path}")
    return df


def generate_holidays() -> pd.DataFrame:
    """Export holiday calendar from config."""
    print("Generating holiday calendar...")
    rows = []
    for i, (hdate, hname, is_national) in enumerate(HOLIDAYS, 1):
        rows.append({
            "id": i,
            "holiday_date": hdate.strftime("%Y-%m-%d"),
            "name": hname,
            "is_national": is_national,
            "is_company": False,
            "affects_locations": "all",
        })
    df = pd.DataFrame(rows)
    output_path = os.path.join(OUTPUT_DIR, "holiday_calendar.csv")
    df.to_csv(output_path, index=False)
    print(f"  Saved {len(df):,} holidays to {output_path}")
    return df


def generate_daily_menus() -> tuple:
    """Generate daily menus and menu items for each location."""
    print("Generating daily menus...")
    days = (END_DATE - START_DATE).days + 1
    menu_rows = []
    item_rows = []
    menu_id = 1
    item_id = 1

    # Meal IDs by period (matching schema seed)
    hot_breakfast = [9, 10, 11, 12]
    hot_lunch = [1, 2, 3, 4, 5, 7, 8]
    hot_dinner = [6, 13, 14, 15, 16]
    cold_any = [17, 18, 19, 20]

    for day_offset in range(days):
        d = START_DATE + timedelta(days=day_offset)
        for loc_id in range(1, len(LOCATIONS) + 1):
            menu_rows.append({
                "id": menu_id,
                "menu_date": d.strftime("%Y-%m-%d"),
                "location_id": loc_id,
                "created_by": None,
                "notes": None,
            })

            # Pick 2-3 hot items per period + 1-2 cold
            for meal_id in np.random.choice(hot_breakfast, size=2, replace=False):
                item_rows.append({"id": item_id, "menu_id": menu_id,
                                  "meal_type_id": int(meal_id), "planned_quantity": 0, "price": 0})
                item_id += 1
            for meal_id in np.random.choice(hot_lunch, size=3, replace=False):
                item_rows.append({"id": item_id, "menu_id": menu_id,
                                  "meal_type_id": int(meal_id), "planned_quantity": 0, "price": 0})
                item_id += 1
            for meal_id in np.random.choice(hot_dinner, size=2, replace=False):
                item_rows.append({"id": item_id, "menu_id": menu_id,
                                  "meal_type_id": int(meal_id), "planned_quantity": 0, "price": 0})
                item_id += 1
            for meal_id in np.random.choice(cold_any, size=2, replace=False):
                item_rows.append({"id": item_id, "menu_id": menu_id,
                                  "meal_type_id": int(meal_id), "planned_quantity": 0, "price": 0})
                item_id += 1

            menu_id += 1

    menu_df = pd.DataFrame(menu_rows)
    item_df = pd.DataFrame(item_rows)
    menu_df.to_csv(os.path.join(OUTPUT_DIR, "daily_menus.csv"), index=False)
    item_df.to_csv(os.path.join(OUTPUT_DIR, "menu_items.csv"), index=False)
    print(f"  Saved {len(menu_df):,} menus, {len(item_df):,} menu items")
    return menu_df, item_df


if __name__ == "__main__":
    generate_events()
    generate_visitors()
    generate_holidays()
    generate_daily_menus()
