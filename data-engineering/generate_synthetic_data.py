"""
Main Synthetic Data Generation Orchestrator
Runs all generators in order and produces complete dataset.
Usage: python generate_synthetic_data.py
"""
import time
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import OUTPUT_DIR
from generators.employees import generate_employees
from generators.weather import generate_weather
from generators.visitors import generate_events, generate_visitors, generate_holidays, generate_daily_menus
from generators.meals import generate_attendance_and_meals


def main():
    print("=" * 60)
    print("  AI Meal Demand — Synthetic Data Generator")
    print("=" * 60)
    start = time.time()

    # Step 1: Employees
    print("\n[1/6] Generating employees...")
    emp_df = generate_employees()

    # Step 2: Weather
    print("\n[2/6] Generating weather data...")
    weather_df = generate_weather()

    # Step 3: Holidays
    print("\n[3/6] Generating holiday calendar...")
    generate_holidays()

    # Step 4: Events & Visitors
    print("\n[4/6] Generating events & visitors...")
    generate_events()
    generate_visitors()

    # Step 5: Daily Menus
    print("\n[5/6] Generating daily menus...")
    generate_daily_menus()

    # Step 6: Attendance & Meal Transactions (depends on employees + weather)
    print("\n[6/6] Generating attendance & meal transactions...")
    generate_attendance_and_meals(emp_df, weather_df)

    elapsed = time.time() - start
    print("\n" + "=" * 60)
    print(f"  COMPLETE — Total time: {elapsed:.1f}s")
    print(f"  Output directory: {OUTPUT_DIR}")
    print("=" * 60)

    # Summary
    print("\nGenerated files:")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.endswith(".csv"):
            size = os.path.getsize(os.path.join(OUTPUT_DIR, f))
            size_mb = size / (1024 * 1024)
            print(f"  {f:30s} {size_mb:8.1f} MB")


if __name__ == "__main__":
    main()
