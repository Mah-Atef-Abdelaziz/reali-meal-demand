---
title: REAL.i Meal Demand AI
emoji: 🍽️
colorFrom: yellow
colorTo: gray
sdk: docker
app_port: 7860
pinned: false
---

<div align="center">

# REAL.i — AI-Powered Meal Demand Prediction System

**Enterprise Intelligent Food Service Optimization Platform**

[![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-16.2+-black?logo=nextdotjs)](https://nextjs.org)
[![XGBoost](https://img.shields.io/badge/XGBoost-R²_0.98-orange)](https://xgboost.readthedocs.io)
[![License](https://img.shields.io/badge/License-Proprietary-gold)]()

</div>

---

## Overview

REAL.i is a full-stack enterprise AI system designed to predict daily meal demand across 15 operational facilities (offices, onshore plants, and offshore platforms). It reduces food waste by **24.5%**, saves an estimated **148,500 SAR/month**, and provides explainable predictions through an integrated SHAP-powered analytics dashboard and RAG-based conversational AI assistant.

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    REAL.i System Architecture                 │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐  │
│  │  Next.js 16  │◄──►│  FastAPI    │◄──►│  SQLite / PG    │  │
│  │  Frontend    │    │  Backend    │    │  Database       │  │
│  │  (Port 3000) │    │  (Port 8000)│    │  (1.4M records) │  │
│  └─────────────┘    └──────┬──────┘    └─────────────────┘  │
│                            │                                 │
│                     ┌──────┴──────┐                          │
│                     │  ML Engine  │                          │
│                     │  XGBoost    │                          │
│                     │  SHAP       │                          │
│                     │  38 Features│                          │
│                     └─────────────┘                          │
└──────────────────────────────────────────────────────────────┘
```

## Features

| Module | Description |
|--------|-------------|
| **ML Forecasting** | XGBoost regression model with R² = 0.9820 and MAE = 3.75 meals |
| **Explainable AI** | SHAP-based feature importance and natural language explanations |
| **Smart Assistant** | RAG-ready chatbot with contextual meal demand Q&A |
| **Dashboard** | Real-time KPIs, waste trends, period distribution, location capacity |
| **Predictions** | Interactive forecast panel with SHAP contribution visualization |
| **Menu Planning** | Daily menu configuration and visitor meal planning |
| **Reports** | CSV/Excel export for consumption, waste, and accuracy logs |
| **Auth & RBAC** | JWT authentication with role-based access control |

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Next.js 16, React 19, TypeScript, Tailwind CSS 4, Recharts, Lucide Icons |
| **Backend** | FastAPI, SQLAlchemy (async), Pydantic, Uvicorn |
| **Database** | SQLite (dev) / PostgreSQL 16 (prod) |
| **ML/AI** | scikit-learn, XGBoost, SHAP, pandas, NumPy |
| **Auth** | JWT (python-jose), passlib (sha256_crypt) |
| **DevOps** | Docker, Docker Compose |

## Project Structure

```
NLP/
├── backend/                    # FastAPI application
│   ├── main.py                 # Entry point with lifespan management
│   ├── config.py               # Environment-based settings (Pydantic)
│   ├── database.py             # SQLAlchemy async engine & session
│   ├── models/                 # ORM models (18 tables)
│   ├── schemas/                # Pydantic request/response schemas
│   ├── routers/                # API endpoint routers
│   │   ├── auth.py             # Login, register, token refresh
│   │   ├── dashboard.py        # KPIs, trends, public summary endpoints
│   │   ├── predictions.py      # ML forecast generation
│   │   ├── chatbot.py          # Smart assistant chat interface
│   │   ├── employees.py        # Employee management
│   │   ├── recommendations.py  # AI-generated recommendations
│   │   └── reports.py          # Report generation & export
│   ├── services/               # Business logic layer
│   │   ├── prediction_service.py   # ML model loading & inference
│   │   ├── chatbot_service.py      # RAG/LLM integration
│   │   ├── recommendation_engine.py # Smart recommendations
│   │   └── report_generator.py     # PDF/Excel report builder
│   └── auth/                   # JWT handler & RBAC utilities
│
├── frontend/                   # Next.js 16 application
│   └── src/
│       ├── app/                # App Router (layout, page, globals.css)
│       ├── components/         # UI components
│       │   ├── Sidebar.tsx         # Navigation sidebar
│       │   ├── DashboardView.tsx   # Analytics dashboard
│       │   ├── PredictionsView.tsx # Forecast interface
│       │   ├── ChatbotView.tsx     # Smart assistant
│       │   ├── MenusView.tsx       # Menu planning
│       │   ├── ReportsView.tsx     # Export & audit logs
│       │   └── SettingsView.tsx    # System configuration
│       └── lib/
│           └── api.ts          # API client with mock fallback
│
├── ml/                         # Machine Learning pipeline
│   ├── preprocessing.py        # Feature engineering (38 features)
│   ├── model_comparison.py     # Algorithm comparison & tuning
│   ├── explainability.py       # SHAP analysis & visualization
│   ├── models/                 # Trained model artifacts (.joblib)
│   └── processed/              # Processed datasets & feature lists
│
├── data-engineering/           # Synthetic data generation
│   ├── generators/             # Per-entity data generators
│   ├── config.py               # Generation profiles & parameters
│   ├── run_all.py              # Orchestrator script
│   ├── load_db.py              # CSV → SQLite bulk loader
│   └── output/                 # Generated CSV files
│
├── database/
│   └── schema.sql              # PostgreSQL DDL schema (425 lines)
│
├── Dockerfile                  # Multi-stage Docker build
├── docker-compose.yml          # Service orchestration
└── README.md                   # This file
```

## Quick Start

### Prerequisites
- Python 3.12+
- Node.js 20+
- npm 10+

### 1. Generate Synthetic Data
```bash
cd data-engineering
python run_all.py
```

### 2. Run ML Pipeline
```bash
python ml/preprocessing.py
python ml/model_comparison.py
python ml/explainability.py
```

### 3. Seed Database
```bash
python data-engineering/load_db.py
```

### 4. Start Backend
```bash
python backend/main.py
# API available at http://localhost:8000
# Swagger docs at http://localhost:8000/docs
```

### 5. Start Frontend
```bash
cd frontend
npm install
npm run dev
# Dashboard available at http://localhost:3000
```

### Docker (Alternative)
```bash
docker-compose up --build
```

## API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/health` | No | System health check |
| `GET` | `/ready` | No | Readiness probe (DB + ML model) |
| `GET` | `/api/v1/dashboard/summary` | No | Dashboard KPI summary |
| `GET` | `/api/v1/dashboard/locations` | No | Location demand capacity |
| `GET` | `/api/v1/dashboard/periods` | No | Meal period distribution |
| `GET` | `/api/v1/dashboard/waste` | No | Weekly waste trend |
| `GET` | `/api/v1/predictions/forecast` | No | Single forecast query |
| `POST` | `/api/v1/chatbot/message` | No | Smart assistant message |
| `POST` | `/api/v1/auth/login` | No | JWT login |
| `POST` | `/api/v1/predictions/predict` | JWT | Batch prediction generation |
| `GET` | `/api/v1/dashboard/kpis` | JWT | Detailed KPI metrics |
| `GET` | `/api/v1/employees/` | JWT | Employee listing |

## ML Model Performance

| Model | R² | MAE | RMSE | MAPE |
|-------|-----|-----|------|------|
| **XGBoost** ★ | **0.9820** | **3.75** | 7.06 | 22.21% |
| Random Forest | 0.9724 | 5.12 | 8.73 | 28.59% |
| Linear Regression | 0.9148 | 9.49 | 15.35 | 38.72% |

## Database Schema

- **18 normalized tables** (3NF)
- **1,470,238 total records** across all tables
- Key tables: `employees` (100K), `meal_transactions` (1M+), `attendance` (210K), `weather_data` (11K)

## Default Credentials

| Username | Password | Role |
|----------|----------|------|
| `admin` | `admin123` | Administrator |

> ⚠️ **Change default credentials in production!**

## License

Proprietary — REAL Intelligence © 2026. All rights reserved.
