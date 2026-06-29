"""
Seeder script to transfer data from local SQLite database to Neon PostgreSQL database.
"""
import os
import sys
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table

# Add backend and project root directories to path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(root_dir, 'backend'))
sys.path.insert(1, root_dir)

# Absolute path to meal_demand.db in the project root
db_path = os.path.abspath(os.path.join(root_dir, "meal_demand.db"))
SQLITE_URL = f"sqlite:///{db_path}"
POSTGRES_URL = "postgresql://neondb_owner:npg_iEgXjo8fC2Zp@ep-holy-union-abdek8zs.eu-west-2.aws.neon.tech/neondb?sslmode=require"

def main():
    print("Connecting to source SQLite and target PostgreSQL...")
    sqlite_engine = create_engine(SQLITE_URL)
    postgres_engine = create_engine(POSTGRES_URL)

    # Reflect schemas
    from database import Base
    from models import (
        Department, WorkLocation, Employee, MealType, DailyMenu, MenuItem,
        Attendance, MealTransaction, WeatherData, HolidayCalendar,
        CompanyEvent, Visitor, PredictionResult, ModelLog, User,
        Feedback, ChatSession, ChatMessage, AuditLog, Notification
    )
    
    print("Constructing database tables on target PostgreSQL (Neon)...")
    Base.metadata.create_all(postgres_engine)

    sqlite_meta = MetaData()
    sqlite_meta.reflect(bind=sqlite_engine)

    # List of tables in correct topological order to respect foreign key constraints
    ordered_tables = [
        "departments",
        "work_locations",
        "employees",
        "meal_types",
        "daily_menus",
        "menu_items",
        "attendance",
        "meal_transactions",
        "weather_data",
        "holiday_calendar",
        "company_events",
        "visitors",
        "prediction_results",
        "model_logs",
        "users",
        "feedback",
        "chat_sessions",
        "chat_messages",
        "audit_logs",
        "notifications"
    ]

    print("Beginning data migration. Please wait...")
    for table_name in ordered_tables:
        if table_name not in sqlite_meta.tables:
            print(f"Table {table_name} not found in SQLite. Skipping...")
            continue
            
        print(f"Migrating table: {table_name}...")
        
        # Read from SQLite in chunks to prevent memory overflow
        chunksize = 50000 if table_name == "meal_transactions" else 10000
        
        # First clear target table
        with postgres_engine.connect() as conn:
            try:
                conn.execute(Table(table_name, sqlite_meta, autoload_with=postgres_engine).delete())
                conn.commit()
            except Exception as e:
                print(f"  Note while clearing {table_name}: {e}")

        # Stream chunks from SQLite to PostgreSQL
        total_rows = 0
        for chunk in pd.read_sql_table(table_name, sqlite_engine, chunksize=chunksize):
            chunk.to_sql(
                name=table_name,
                con=postgres_engine,
                if_exists="append",
                index=False,
                method="multi",
                chunksize=1000  # fast multi-row inserts
            )
            total_rows += len(chunk)
            print(f"  Uploaded {total_rows} rows...")
            
    print("Migration completed successfully!")

if __name__ == "__main__":
    main()
