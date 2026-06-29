"""
Database Loader — Imports generated synthetic CSV data into the SQLite database.
"""
import os
import sys
import pandas as pd
from sqlalchemy import select, text
import os
import sys
workspace = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(workspace, "backend"))
sys.path.insert(0, workspace)

from database import sync_engine, Base
from models import (
    Department, WorkLocation, Employee, MealType, DailyMenu, MenuItem,
    Attendance, MealTransaction, WeatherData, HolidayCalendar, CompanyEvent,
    Visitor, User
)
from auth import hash_password

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")


def seed_core_data(session):
    """Seed departments, locations, and meal types if not already seeded."""
    print("Seeding core metadata tables...")
    
    # Load data-engineering config.py dynamically
    import importlib.util
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.py")
    spec = importlib.util.spec_from_file_location("data_config", config_path)
    data_config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(data_config)
    
    # 1. Departments
    existing_depts = session.execute(select(Department.code)).scalars().all()
    for name, code in data_config.DEPARTMENTS:
        if code not in existing_depts:
            dept = Department(name=name, code=code, head_name=f"Head of {name}")
            session.add(dept)
            
    # 2. Locations
    existing_locs = session.execute(select(WorkLocation.code)).scalars().all()
    for name, code, type_, city, cap in data_config.LOCATIONS:
        if code not in existing_locs:
            loc = WorkLocation(
                name=name, code=code, location_type=type_, city=city,
                capacity=cap, latitude=None, longitude=None
            )
            session.add(loc)
            
    # 3. Meal Types
    meal_types = [
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
        ('Yogurt Parfait', 'dairy', 'cold', 'breakfast', 4.00, 5)
    ]
    existing_meals = session.execute(select(MealType.name)).scalars().all()
    for name, cat, temp, period, cost, prep in meal_types:
        if name not in existing_meals:
            meal = MealType(
                name=name, category=cat, temperature=temp, period=period,
                estimated_cost=cost, preparation_time_minutes=prep
            )
            session.add(meal)
            
    # 4. Default Admin User
    existing_admin = session.execute(select(User).where(User.username == "admin")).scalar_one_or_none()
    if not existing_admin:
        admin = User(
            username="admin",
            email="admin@real-i.com",
            password_hash=hash_password("admin123"),
            role="admin",
            is_active=True
        )
        session.add(admin)

    session.commit()
    print("Core metadata tables seeded.")


def load_csv_to_db():
    """Load all generated CSV files into the database."""
    from sqlalchemy.orm import Session
    
    # Verify tables are created first
    Base.metadata.create_all(bind=sync_engine)
    
    with Session(sync_engine) as session:
        seed_core_data(session)
        
        # Load tables
        table_mappings = [
            ("employees.csv", Employee, "employees"),
            ("weather_data.csv", WeatherData, "weather_data"),
            ("holiday_calendar.csv", HolidayCalendar, "holiday_calendar"),
            ("visitors.csv", Visitor, "visitors"),
            ("company_events.csv", CompanyEvent, "company_events"),
            ("daily_menus.csv", DailyMenu, "daily_menus"),
            ("menu_items.csv", MenuItem, "menu_items"),
            ("attendance.csv", Attendance, "attendance"),
            ("meal_transactions.csv", MealTransaction, "meal_transactions"),
        ]
        
        for csv_file, model, table_name in table_mappings:
            path = os.path.join(DATA_DIR, csv_file)
            if not os.path.exists(path):
                print(f"Skipping {csv_file}: File not found.")
                continue
                
            # Check if table already has data
            count = session.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
            if count > 0:
                print(f"Table '{table_name}' already contains {count} records. Skipping loading.")
                continue
                
            print(f"Loading {csv_file} into table '{table_name}'...")
            
            # Read CSV in chunks for efficiency
            chunksize = 50000
            for chunk in pd.read_csv(path, chunksize=chunksize):
                # Convert dates if needed
                for col in chunk.columns:
                    if col.endswith("_date") or col in ["hire_date", "check_in", "check_out", "created_at"]:
                        chunk[col] = pd.to_datetime(chunk[col], errors="coerce")
                        
                # Handle any boolean conversions or nan values
                chunk = chunk.where(pd.notnull(chunk), None)
                
                # Insert chunk using pandas to_sql or raw insert
                # pandas to_sql is easiest but we need to ensure correct columns
                records = chunk.to_dict(orient="records")
                session.bulk_insert_mappings(model, records)
                session.commit()
                
            final_count = session.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
            print(f"Successfully loaded {final_count} records into '{table_name}'.")

    print("\nDatabase load complete.")


if __name__ == "__main__":
    load_csv_to_db()
