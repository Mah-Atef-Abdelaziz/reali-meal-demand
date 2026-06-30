import collections, collections.abc, os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# ── Color Palette ──
BG_DARK = RGBColor(18, 19, 24)
CARD_BG = RGBColor(26, 28, 35)
GOLD = RGBColor(222, 193, 92)
WHITE = RGBColor(255, 255, 255)
MUTED = RGBColor(163, 163, 163)
BORDER = RGBColor(60, 62, 74)

SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), "docs", "screenshots")

def bg(slide):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    s.fill.solid(); s.fill.fore_color.rgb = BG_DARK; s.line.fill.background()

def title(slide, text):
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.8))
    p = tb.text_frame.paragraphs[0]; p.text = text
    p.font.name = 'Montserrat'; p.font.size = Pt(36); p.font.bold = True; p.font.color.rgb = GOLD

def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text

def card(slide, x, y, w, h, border_color=BORDER):
    c = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    c.fill.solid(); c.fill.fore_color.rgb = CARD_BG; c.line.color.rgb = border_color; return c

def textbox(slide, x, y, w, h):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tb.text_frame.word_wrap = True
    tb.text_frame.margin_left = tb.text_frame.margin_top = tb.text_frame.margin_bottom = tb.text_frame.margin_right = 0
    return tb.text_frame

def add_heading(tf, text):
    p = tf.paragraphs[0]; p.text = text
    p.font.name = 'Montserrat'; p.font.size = Pt(20); p.font.bold = True; p.font.color.rgb = GOLD

def add_bullets(tf, items, color=WHITE, size=15):
    for b in items:
        p = tf.add_paragraph(); p.text = "• " + b
        p.font.name = 'Calibri'; p.font.size = Pt(size); p.font.color.rgb = color; p.space_before = Pt(10)

def screenshot_slide(slide, img_path, title_text, note_text):
    """Add a full-width screenshot slide with a title bar and speaker notes."""
    bg(slide)
    # Title bar
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(1.1))
    bar.fill.solid(); bar.fill.fore_color.rgb = CARD_BG; bar.line.fill.background()
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.2), Inches(11), Inches(0.7))
    p = tb.text_frame.paragraphs[0]; p.text = title_text
    p.font.name = 'Montserrat'; p.font.size = Pt(30); p.font.bold = True; p.font.color.rgb = GOLD
    # Screenshot image centered
    if os.path.exists(img_path):
        slide.shapes.add_picture(img_path, Inches(1.0), Inches(1.3), Inches(11.333), Inches(5.9))
    notes(slide, note_text)

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    # ═══════════════════════════════════════════════════════
    # SLIDE 1: Title
    # ═══════════════════════════════════════════════════════
    s = prs.slides.add_slide(blank); bg(s)
    a = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(2.2), Inches(0.15), Inches(3.2))
    a.fill.solid(); a.fill.fore_color.rgb = GOLD; a.line.fill.background()
    tf = textbox(s, Inches(1.2), Inches(2.1), Inches(11), Inches(3.5))
    p = tf.paragraphs[0]; p.text = "REAL.i"; p.font.name = 'Montserrat'; p.font.size = Pt(64); p.font.bold = True; p.font.color.rgb = GOLD
    p2 = tf.add_paragraph(); p2.text = "MEAL DEMAND AI FORECASTING PLATFORM"; p2.font.name = 'Montserrat'; p2.font.size = Pt(22); p2.font.bold = True; p2.font.color.rgb = WHITE; p2.space_before = Pt(10)
    p3 = tf.add_paragraph(); p3.text = "Enterprise AI System to Optimize Catering Operations, Reduce Waste & Lower Costs"; p3.font.name = 'Calibri'; p3.font.size = Pt(16); p3.font.color.rgb = MUTED; p3.space_before = Pt(15)
    p4 = tf.add_paragraph(); p4.text = "Egypt • 15 Corporate Locations • 1.47M Transaction Records"; p4.font.name = 'Calibri'; p4.font.size = Pt(14); p4.font.bold = True; p4.font.color.rgb = GOLD; p4.space_before = Pt(30)
    notes(s, """SPEAKER SCRIPT — SLIDE 1: Title & Introduction

"Welcome everyone. Today we are presenting REAL.i — an enterprise-grade AI forecasting system built to solve a multi-million dollar corporate catering challenge: food waste.

When catering at scale across 15 operational facilities — offices, industrial plants, and field sites — traditional guesswork leads to a baseline 30% food waste rate. REAL.i transforms this guesswork into precision AI forecasting, achieving a 24.5% waste reduction and saving an estimated 148,500 EGP per month.

Let me walk you through how we built it, the technology behind it, and the results it delivers."
""")

    # ═══════════════════════════════════════════════════════
    # SLIDE 2: The Core Problem
    # ═══════════════════════════════════════════════════════
    s = prs.slides.add_slide(blank); bg(s); title(s, "The Catering Scale Challenge")
    card(s, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
    tf = textbox(s, Inches(1.1), Inches(2.1), Inches(5.0), Inches(4.2))
    add_heading(tf, "Operational Difficulties")
    add_bullets(tf, [
        "Traditional catering relies on static headcounts, leading to massive inefficiencies.",
        "Over-preparation results in a baseline 30% food waste rate.",
        "Under-preparation leads to portion shortages and damages employee satisfaction.",
        "Industrial plants & field sites have complex 14-day shift rotation schedules."
    ])
    card(s, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8))
    tf2 = textbox(s, Inches(7.1), Inches(2.1), Inches(5.1), Inches(4.2))
    add_heading(tf2, "Key Forecasting Drivers")
    add_bullets(tf2, [
        "Rotational Shifts: Day/Night rotations dynamically impact headcount.",
        "Weather Conditions: Hot temperatures shift demand from hot food to salads.",
        "Calendar Events: Egyptian national holidays & corporate workshops.",
        "Location Capacities: Distinguishing office space from remote industrial sites."
    ])
    notes(s, """SPEAKER SCRIPT — SLIDE 2: The Core Problem

"Why is this problem so hard? Because corporate locations aren't static environments. In field sites, crews rotate every 14 days. In offices, people work Sunday-to-Thursday — that's already different from the standard Monday-to-Friday calendar most systems assume.

Weather matters too — when temperatures exceed 40°C, employees shift preference from heavy rice dishes to lighter salads and cold plates. Then there are national holidays, visitor schedules, and site-specific seating capacities to consider.

Without data-driven forecasting, kitchens rely on fixed headcounts, resulting in a baseline 30% waste rate. At an average cost of 15 EGP per meal across 15 locations, that waste adds up to hundreds of thousands of pounds every month."
""")

    # ═══════════════════════════════════════════════════════
    # SLIDE 3: System Architecture
    # ═══════════════════════════════════════════════════════
    s = prs.slides.add_slide(blank); bg(s); title(s, "Decoupled System Architecture")
    layers = [
        ("Frontend UI", "Next.js 16 Console", ["React 19 App Router dashboard.", "Gold/charcoal micro-animations.", "Mobile-responsive sidebar with '<' and '^' controls.", "Real-time KPIs, savings charts, predictions."]),
        ("Backend API", "FastAPI Core Engine", ["Async runtime using Python 3.12.", "Asyncpg for non-blocking database queries.", "OpenAI GPT-4o-mini LangChain RAG integration.", "Docker container on Hugging Face Spaces (Port 7860)."]),
        ("Database Layer", "Neon Serverless Postgres", ["18-table 3NF relational database.", "1.47 million historical records.", "Audit logs, predictions, weather, rosters.", "Auto-scaling keeps infrastructure cost at zero."])
    ]
    for i, (t, sub, bullets) in enumerate(layers):
        x = Inches(0.8) + i * (Inches(3.64) + Inches(0.4))
        card(s, x, Inches(1.8), Inches(3.64), Inches(4.8))
        tf = textbox(s, x + Inches(0.25), Inches(2.0), Inches(3.14), Inches(4.4))
        add_heading(tf, t)
        p = tf.add_paragraph(); p.text = sub; p.font.name = 'Calibri'; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = WHITE; p.space_before = Pt(4)
        add_bullets(tf, bullets, MUTED, 13)
    notes(s, """SPEAKER SCRIPT — SLIDE 3: System Architecture

"REAL.i is built as a fully decoupled, production-grade system with three distinct layers.

The Frontend is a Next.js 16 application using React 19 with the App Router pattern. It features a premium gold-and-charcoal design with smooth micro-animations, and is fully mobile-responsive.

The Backend is a FastAPI engine running Python 3.12 with fully asynchronous database queries via asyncpg — meaning zero blocking when serving multiple concurrent requests. It integrates with OpenAI's GPT-4o-mini through LangChain for our conversational AI assistant.

The Database Layer uses Neon Serverless PostgreSQL — a managed, auto-scaling cloud database containing our entire 1.47 million transaction records across 18 normalized tables. The best part? Zero infrastructure maintenance cost."
""")

    # ═══════════════════════════════════════════════════════
    # SLIDE 4: Screenshot — Dashboard
    # ═══════════════════════════════════════════════════════
    s = prs.slides.add_slide(blank)
    screenshot_slide(s, os.path.join(SCREENSHOTS_DIR, "dashboard.png"), "Live Dashboard — Operational Overview",
"""SPEAKER SCRIPT — SLIDE 4: Live Dashboard Demo

"Here is the live REAL.i dashboard. As you can see, it displays four key operational KPIs at the top:
- Total Forecasts generated: 1,450
- Waste Reduction rate: 30% (down from baseline)
- Cost Savings: 148,500 EGP
- Model Accuracy: 96.8%

Below that, we have two interactive charts:
1. A bar chart showing Daily Prepared vs Wasted Meals across the week — you can clearly see waste trending downward from Sunday to Thursday.
2. A donut chart showing Meal Period Demand Share — Lunch dominates at 98,450 meals, followed by Dinner and Breakfast.

Notice the 'System Status: ONLINE' indicator at the bottom left — this confirms the frontend is actively connected to our FastAPI backend. The active model badge in the top right shows 'XGBoost-Regressor v1.0.0'."
""")

    # ═══════════════════════════════════════════════════════
    # SLIDE 5: Screenshot — Collapsed Sidebar
    # ═══════════════════════════════════════════════════════
    s = prs.slides.add_slide(blank)
    screenshot_slide(s, os.path.join(SCREENSHOTS_DIR, "dashboard_collapsed.png"), "Mobile-Responsive Sidebar — Collapsed View",
"""SPEAKER SCRIPT — SLIDE 5: Responsive Sidebar

"One important design decision was mobile responsiveness. On desktop, the sidebar can be collapsed using the '<' button, shrinking it to a compact icon-only rail. This gives the analytics content more screen real estate.

On mobile devices, the sidebar converts to a slide-over drawer that opens with '<' and closes with '^'. This ensures kitchen supervisors using tablets or phones in the field can navigate comfortably without the menu blocking their dashboard view.

The sidebar automatically closes when a navigation item is selected on mobile."
""")

    # ═══════════════════════════════════════════════════════
    # SLIDE 6: ML Feature Engineering
    # ═══════════════════════════════════════════════════════
    s = prs.slides.add_slide(blank); bg(s); title(s, "Machine Learning — Feature Engineering")
    card(s, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
    tf = textbox(s, Inches(1.1), Inches(2.1), Inches(5.0), Inches(4.2))
    add_heading(tf, "38 Engineered Feature Vectors")
    add_bullets(tf, [
        "Temporal: Month, day of week, day of year, quarter.",
        "Egypt Work Week: Custom 'egypt_dow' maps Sun-Thu cycle.",
        "Lag Indicators: 1-day, 7-day, 14-day, 28-day historical lags.",
        "Rolling Averages: 7-day and 14-day moving demand averages."
    ])
    card(s, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8))
    tf2 = textbox(s, Inches(7.1), Inches(2.1), Inches(5.1), Inches(4.2))
    add_heading(tf2, "Environmental & External Inputs")
    add_bullets(tf2, [
        "Site Capacity: Max seating thresholds per location.",
        "Weather: Average temperature, humidity, rainfall.",
        "Holiday Calendars: National holidays and company events.",
        "Visitor Log: Scheduled external visitor counts.",
        "Department Metrics: Roster counts per department."
    ], MUTED)
    notes(s, """SPEAKER SCRIPT — SLIDE 6: Feature Engineering

"The core of our ML pipeline is a 38-feature vector engineered from multiple data layers.

First, temporal features — standard ones like month, day of week, quarter. But critically, we built a custom 'egypt_dow' feature. Standard libraries treat Monday as the start of the work week, but in Egypt, work runs Sunday through Thursday. Our custom feature correctly maps weekend drops to Friday and Saturday.

Second, lag indicators. We feed the model what happened 1 day ago, 7 days ago, 14 days ago, and 28 days ago at the same location and meal period. This captures weekly cyclical patterns.

Third, rolling averages — 7-day and 14-day moving averages smooth out noise and detect gradual shifts in demand.

Finally, environmental inputs: weather data, holiday calendars, visitor schedules, and site capacity constraints all feed into the model."
""")

    # ═══════════════════════════════════════════════════════
    # SLIDE 7: Model Performance
    # ═══════════════════════════════════════════════════════
    s = prs.slides.add_slide(blank); bg(s); title(s, "Model Performance & Accuracy")
    card(s, Inches(0.8), Inches(1.8), Inches(6.5), Inches(4.8))
    tf = textbox(s, Inches(1.1), Inches(2.1), Inches(5.9), Inches(4.2))
    add_heading(tf, "Forecasting Algorithm Comparison")
    p = tf.add_paragraph()
    p.text = ("1. XGBoost Regressor (Selected)\n    R² Score: 0.9820  |  MAE: 3.75 meals\n\n"
              "2. Random Forest Regressor\n    R² Score: 0.9724  |  MAE: 5.12 meals\n\n"
              "3. Gradient Boosting Regressor\n    R² Score: 0.9680  |  MAE: 5.95 meals\n\n"
              "4. Linear Regression Baseline\n    R² Score: 0.9148  |  MAE: 9.49 meals")
    p.font.name = 'Calibri'; p.font.size = Pt(14); p.font.color.rgb = WHITE; p.space_before = Pt(15)
    card(s, Inches(7.7), Inches(1.8), Inches(4.8), Inches(4.8), GOLD)
    tf2 = textbox(s, Inches(8.0), Inches(2.1), Inches(4.2), Inches(4.2))
    add_heading(tf2, "Why XGBoost Wins")
    add_bullets(tf2, [
        "Captures complex non-linear relations and feature interactions.",
        "Robust against missing records and outliers.",
        "Config: 500 estimators, max depth 7, learning rate 0.05.",
        "Nightly automatic retraining via feedback loops."
    ])
    notes(s, """SPEAKER SCRIPT — SLIDE 7: Model Performance

"We evaluated four regression algorithms on our dataset. The results speak clearly:

XGBoost achieved an R-squared of 0.9820 with a Mean Absolute Error of just 3.75 meals. That means if the model predicts 1,000 meals, the actual demand will be between 996 and 1,004 meals. That's extraordinary precision.

Random Forest came close at 0.9724, but XGBoost's ability to capture non-linear feature interactions — like the compound effect of hot weather PLUS a Thursday PLUS visitors — gave it the edge.

Linear Regression struggled at 0.9148 because meal demand is fundamentally non-linear.

Our selected XGBoost configuration uses 500 estimators with a max depth of 7 and a learning rate of 0.05. The model automatically retrains nightly through our feedback loop, comparing predictions against actual transaction counts."
""")

    # ═══════════════════════════════════════════════════════
    # SLIDE 8: Screenshot — Predictions with SHAP
    # ═══════════════════════════════════════════════════════
    s = prs.slides.add_slide(blank)
    screenshot_slide(s, os.path.join(SCREENSHOTS_DIR, "predictions_result.png"), "Live Predictions — SHAP Explainability",
"""SPEAKER SCRIPT — SLIDE 8: Predictions with SHAP

"Here's the Predictions module in action. The user selects a Work Location (Headquarters HQ), a Target Date (July 1st, 2026), and a Meal Period (Lunch), then clicks 'Generate Forecast'.

The system returns a Forecast Output Summary showing:
- Predicted Demand count
- Recommended Preparation quantity (with a 5% safety buffer)
- Expected Waste margin
- Confidence Score (94.4%)

On the right side, you can see the SHAP Feature Contributions panel. This is our explainability engine — it shows exactly WHY the model made this prediction:
- 'same_dow_last_week' contributed +45.2% — the strongest driver
- '7-day lag' contributed +32.1%
- 'rolling_mean_7d' contributed +12.5%
- 'temperature_avg' reduced the prediction by -8.1% (hot weather)

This transparency is critical for building trust with kitchen managers."
""")

    # ═══════════════════════════════════════════════════════
    # SLIDE 9: Screenshot — RAG Chatbot
    # ═══════════════════════════════════════════════════════
    s = prs.slides.add_slide(blank)
    screenshot_slide(s, os.path.join(SCREENSHOTS_DIR, "chatbot_response.png"), "RAG Smart Assistant — Conversational AI",
"""SPEAKER SCRIPT — SLIDE 9: RAG Chatbot Demo

"Instead of forcing managers to write SQL queries or navigate complex reports, we built a conversational AI assistant powered by LangChain and GPT-4o-mini.

In this screenshot, the user asked: 'What is tomorrow's lunch forecast?' The system:
1. Parsed the intent and identified the query type (forecast)
2. Executed real-time SQL queries against the PostgreSQL database
3. Retrieved context statistics (historical demand, lag values, weather)
4. Passed everything to GPT-4o-mini to generate a human-readable answer

The response is data-grounded: 'The lunch forecast for Cairo Headquarters tomorrow is 1,720 meals with a confidence score of 95.4%. I recommend preparing 1,806 meals to maintain a safe 5% buffer.'

It even lists the key contributing factors with their SHAP percentages. This is a RAG system — Retrieval Augmented Generation — not hallucinated answers."
""")

    # ═══════════════════════════════════════════════════════
    # SLIDE 10: Screenshot — Menu Planning
    # ═══════════════════════════════════════════════════════
    s = prs.slides.add_slide(blank)
    screenshot_slide(s, os.path.join(SCREENSHOTS_DIR, "menu_planning.png"), "Menu & Visitor Planning Module",
"""SPEAKER SCRIPT — SLIDE 10: Menu & Visitor Planning

"The Menu Planning module allows kitchen managers to configure daily menus per location. Each meal card shows the item name, protein category, calorie count, price in EGP, and the meal period.

On the right side, there's a Visitor Log panel where managers can register expected external visitors — for example, a group of 45 visitors from EGPC for a technical audit. This visitor count feeds directly into the ML model's prediction pipeline.

Below that, the Registered Visitors section shows a history of logged visitor groups, giving operations teams full visibility into external demand drivers.

This module bridges the gap between kitchen operations and AI predictions — managers configure the menu, the AI tells them how much to prepare."
""")

    # ═══════════════════════════════════════════════════════
    # SLIDE 11: Screenshot — Reports & Audit
    # ═══════════════════════════════════════════════════════
    s = prs.slides.add_slide(blank)
    screenshot_slide(s, os.path.join(SCREENSHOTS_DIR, "reports.png"), "Reports & System Audit Logs",
"""SPEAKER SCRIPT — SLIDE 11: Reports & Audit Trail

"The Reports module provides two critical capabilities:

First, Export Reports — managers can select a date range and report type, then export consumption analytics as CSV or Excel files. This integrates with existing corporate reporting workflows.

Second, the Security Audit Trail on the right side shows a real-time log of every system action: login events, report exports, visitor log updates, and daily forecast generation runs. Each entry includes the user, timestamp, and IP address.

At the bottom, you can see system health indicators: the Database Engine (SQLite for local, PostgreSQL for production) and the Security Protocol (JWT-Token Authentication with RBAC Enabled).

This audit trail is essential for enterprise compliance and operational transparency."
""")

    # ═══════════════════════════════════════════════════════
    # SLIDE 12: ROI & Sustainability
    # ═══════════════════════════════════════════════════════
    s = prs.slides.add_slide(blank); bg(s); title(s, "Commercial ROI & Sustainability Impact")
    metrics = [
        ("24.5%", "FOOD WASTE REDUCTION", "Average waste rate drops from 30.0% to 5.5% using XGBoost predictions."),
        ("148.5k EGP", "MONTHLY COST SAVINGS", "Based on average meal cost of 15 EGP across 15 operational locations."),
        ("44.5 tons", "CO₂ FOOTPRINT OFFSET", "Monthly greenhouse gas emissions avoided by reducing daily food disposal.")
    ]
    for i, (val, t, desc) in enumerate(metrics):
        x = Inches(0.8) + i * (Inches(3.64) + Inches(0.4))
        card(s, x, Inches(1.8), Inches(3.64), Inches(4.8), GOLD if i == 1 else BORDER)
        tf = textbox(s, x + Inches(0.25), Inches(2.2), Inches(3.14), Inches(4.0))
        p = tf.paragraphs[0]; p.text = val; p.font.name = 'Montserrat'; p.font.size = Pt(48); p.font.bold = True; p.alignment = PP_ALIGN.CENTER; p.font.color.rgb = GOLD
        p2 = tf.add_paragraph(); p2.text = t; p2.font.name = 'Montserrat'; p2.font.size = Pt(14); p2.font.bold = True; p2.alignment = PP_ALIGN.CENTER; p2.font.color.rgb = WHITE; p2.space_before = Pt(15)
        p3 = tf.add_paragraph(); p3.text = desc; p3.font.name = 'Calibri'; p3.font.size = Pt(13); p3.alignment = PP_ALIGN.CENTER; p3.font.color.rgb = MUTED; p3.space_before = Pt(15)
    notes(s, """SPEAKER SCRIPT — SLIDE 12: ROI & Sustainability

"Let me close with the numbers that matter most to any executive.

First: a 24.5% reduction in food waste. Our baseline was 30% — meaning nearly one-third of all prepared meals were thrown away. With REAL.i, that drops to 5.5%.

Second: 148,500 EGP saved every single month. At 15 EGP per meal across 15 locations, reducing waste by 24.5% translates directly to bottom-line savings. That's 1.78 million EGP annually.

Third: 44.5 tons of CO₂ emissions avoided per month. Food waste is one of the largest contributors to greenhouse gas emissions. By cooking only what's needed, we're not just saving money — we're contributing to corporate sustainability goals.

AI is not a luxury here. It's an investment tool that pays for itself many times over. Thank you."
""")

    # Save
    out = "docs/REAL.i_Meal_Demand_AI_Presentation.pptx"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    prs.save(out)
    print(f"Presentation saved: {out} ({len(prs.slides)} slides)")

if __name__ == '__main__':
    create_deck()
