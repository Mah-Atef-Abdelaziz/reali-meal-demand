# AI-Powered Meal Demand Prediction & Smart Assistant System

## Implementation Plan

A complete production-ready AI system for predicting hot meal demand, reducing food waste, and providing intelligent decision support through an NLP chatbot — built from scratch.

---

## User Review Required

> [!IMPORTANT]
> **Scale & Scope:** This is a full enterprise system with 18 phases. I will build everything locally and make it Docker-deployable. Actual cloud deployment (Phase 16) requires your Azure/AWS credentials and will be configured but not executed without your approval.

> [!IMPORTANT]
> **LLM API Key:** The NLP chatbot (Phase 7) uses LangChain + an OpenAI-compatible LLM. You'll need to provide an API key (OpenAI, Azure OpenAI, or a local model like Ollama). I'll design it to work with any provider. Should I default to **OpenAI** or would you prefer a **local Ollama** setup?

> [!WARNING]
> **Synthetic Data:** Phase 4 generates 100K+ employee records and 2 years of transactions (~millions of rows). This will take significant compute time and disk space (~500MB-1GB). The generation script will be resumable.

## Open Questions

1. **LLM Provider:** OpenAI API, Azure OpenAI, or local Ollama for the chatbot?
2. **Domain name / Azure subscription:** Do you have these ready for Phase 16, or should I just prepare the deployment configs?
3. **Branding:** Should the UI follow your REAL.i brand identity (gold/charcoal, Orbitron/Montserrat) or a fresh design?
4. **Port preferences:** Any specific ports you want the services to run on locally?

---

## Project Directory Structure

```
f:\Real Intelligence\System\NLP\
├── docs/                          # Phase 1 & 17 — Documentation
│   ├── srs.md                     # Software Requirements Specification
│   ├── sdd.md                     # Software Design Document
│   ├── architecture.md            # Architecture Document
│   ├── api-docs.md                # API Documentation
│   ├── deployment-guide.md        # Deployment Guide
│   ├── user-manual.md             # User Manual
│   └── diagrams/                  # Architecture diagrams (Mermaid exports)
│
├── database/                      # Phase 3 — Database Design
│   ├── schema.sql                 # Complete DDL
│   ├── seed.sql                   # Reference data seeds
│   ├── indexes.sql                # Performance indexes
│   └── migrations/                # Alembic migrations
│
├── data-engineering/              # Phase 4 — Synthetic Data
│   ├── generate_synthetic_data.py # Main data generator
│   ├── config.py                  # Generation parameters
│   ├── generators/                # Per-table generators
│   │   ├── employees.py
│   │   ├── attendance.py
│   │   ├── meals.py
│   │   ├── weather.py
│   │   ├── visitors.py
│   │   └── events.py
│   └── output/                    # Generated CSVs
│
├── ml/                            # Phase 5 & 6 — ML + Explainable AI
│   ├── pipeline.py                # Full ML pipeline orchestrator
│   ├── preprocessing.py           # Data preprocessing & feature engineering
│   ├── feature_engineering.py     # Advanced feature creation
│   ├── model_comparison.py        # Multi-model comparison
│   ├── hyperparameter_tuning.py   # Optuna-based tuning
│   ├── evaluation.py              # Metrics & evaluation
│   ├── explainability.py          # SHAP explanations
│   ├── forecaster.py              # Time-series models (LSTM/Transformer)
│   ├── models/                    # Saved model artifacts
│   └── reports/                   # Training reports & plots
│
├── backend/                       # Phase 11 — FastAPI Backend
│   ├── main.py                    # FastAPI app entry
│   ├── config.py                  # Settings & env config
│   ├── database.py                # SQLAlchemy setup
│   ├── auth/                      # Phase 13 — Security
│   │   ├── jwt_handler.py
│   │   ├── permissions.py
│   │   └── middleware.py
│   ├── models/                    # SQLAlchemy ORM models
│   │   ├── employee.py
│   │   ├── meal.py
│   │   ├── prediction.py
│   │   ├── chat.py
│   │   └── ...
│   ├── schemas/                   # Pydantic schemas
│   ├── routers/                   # API route handlers
│   │   ├── auth.py
│   │   ├── employees.py
│   │   ├── meals.py
│   │   ├── predictions.py
│   │   ├── chatbot.py
│   │   ├── reports.py
│   │   ├── recommendations.py
│   │   ├── dashboard.py
│   │   └── admin.py
│   ├── services/                  # Business logic
│   │   ├── prediction_service.py
│   │   ├── recommendation_engine.py  # Phase 8
│   │   ├── report_generator.py       # Phase 10
│   │   └── chatbot_service.py        # Phase 7
│   ├── nlp/                       # Phase 7 — NLP Pipeline
│   │   ├── chain.py               # LangChain RAG chain
│   │   ├── tools.py               # Custom LangChain tools
│   │   ├── prompts.py             # Prompt templates
│   │   ├── vectorstore.py         # FAISS/ChromaDB setup
│   │   └── document_loader.py     # Knowledge base loader
│   ├── utils/
│   │   ├── cache.py               # Redis caching
│   │   └── logger.py              # Structured logging
│   ├── tests/                     # Phase 14 — Testing
│   │   ├── test_auth.py
│   │   ├── test_predictions.py
│   │   ├── test_chatbot.py
│   │   ├── test_reports.py
│   │   └── conftest.py
│   └── requirements.txt
│
├── frontend/                      # Phase 12 — Next.js Frontend
│   ├── src/
│   │   ├── app/                   # Next.js App Router
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx           # Dashboard (home)
│   │   │   ├── predictions/
│   │   │   ├── reports/
│   │   │   ├── employees/
│   │   │   ├── menus/
│   │   │   ├── analytics/
│   │   │   ├── chatbot/
│   │   │   ├── settings/
│   │   │   └── admin/
│   │   ├── components/            # Reusable UI components
│   │   │   ├── layout/
│   │   │   ├── charts/
│   │   │   ├── tables/
│   │   │   └── chatbot/
│   │   ├── lib/                   # API client, utils
│   │   └── styles/                # Global CSS
│   ├── public/                    # Static assets
│   ├── package.json
│   └── next.config.js
│
├── docker/                        # Phase 15 — DevOps
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   ├── Dockerfile.ml
│   └── nginx.conf
│
├── .github/                       # Phase 15 — CI/CD
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
│
├── monitoring/                    # Phase 15 — Monitoring
│   ├── prometheus.yml
│   └── grafana/
│       └── dashboards/
│
├── docker-compose.yml             # Full stack orchestration
├── docker-compose.dev.yml         # Development overrides
├── .env.example                   # Environment template
├── README.md                      # Project README
└── Makefile                       # Common commands
```

---

## Proposed Changes — Execution Batches

I'll build this in **5 batches**, each producing a working increment:

---

### Batch 1: Foundation (Phases 1–4)
*System Analysis, Architecture, Database, Synthetic Data*

#### [NEW] `docs/srs.md`
- Complete Software Requirements Specification extracted from the task document
- Business problem, stakeholders, functional/non-functional requirements, user stories, use cases, AI opportunities, risks, assumptions

#### [NEW] `docs/architecture.md`
- System architecture document with Mermaid diagrams
- Backend, frontend, AI, NLP, ML, database, deployment architectures

#### [NEW] `database/schema.sql`
- Complete normalized PostgreSQL schema with 18+ tables:
  - `employees`, `departments`, `work_locations`, `meal_types`, `daily_menus`, `menu_items`
  - `attendance`, `meal_transactions`, `employee_eligibility`, `employee_schedules`
  - `weather_data`, `holiday_calendar`, `company_events`, `visitors`
  - `prediction_results`, `model_logs`, `feedback`, `chat_history`
  - `audit_logs`, `notifications`, `users`, `roles`
- All constraints (PK, FK, CHECK, UNIQUE), indexes, and triggers

#### [NEW] `database/indexes.sql`
- Performance indexes on high-query columns

#### [NEW] `data-engineering/` (all files)
- Synthetic data generators producing:
  - 100,000 employees across 20 departments, 15 locations (offshore/onshore/office)
  - 730 days × daily menus with realistic meal rotation
  - ~2M+ meal transaction records with realistic patterns (day-of-week, weather, holiday effects)
  - Attendance records correlated with transactions
  - Weather data (temperature, conditions) per location per day
  - Holiday calendars, company events, visitor records
- Output as CSV files ready for DB import

---

### Batch 2: AI Core (Phases 5–6, 8)
*ML Pipeline, Explainable AI, Smart Recommendations*

#### [NEW] `ml/preprocessing.py`
- Load synthetic data, handle missing values, encode categoricals
- Time-based train/val/test split (last 30 days = test)

#### [NEW] `ml/feature_engineering.py`
- 50+ engineered features: lag features, rolling averages, day-of-week encoding, holiday proximity, weather interactions, menu embeddings, department-level aggregates

#### [NEW] `ml/model_comparison.py`
- Train & compare: XGBoost, LightGBM, CatBoost, Random Forest, Gradient Boosting
- Evaluate with MAE, RMSE, MAPE, R²
- Cross-validation with time-series aware splits

#### [NEW] `ml/forecaster.py`
- LSTM and Transformer-based time-series models using PyTorch
- Compare against gradient boosting baselines

#### [NEW] `ml/hyperparameter_tuning.py`
- Optuna-based hyperparameter search for the top-2 models
- Save best model with joblib/pickle

#### [NEW] `ml/explainability.py`
- SHAP values computation for the best model
- Feature importance plots
- Natural language explanation generator ("prediction increased because...")

#### [NEW] `ml/pipeline.py`
- End-to-end orchestrator: load → preprocess → engineer → train → evaluate → explain → save

#### [NEW] `backend/services/recommendation_engine.py`
- Rule-based + ML-informed recommendation engine
- Generates actionable recommendations: reduce/increase quantities, waste alerts, menu optimization

---

### Batch 3: Backend & NLP (Phases 7, 10, 11, 13)
*FastAPI Backend, NLP Chatbot, Reports, Security*

#### [NEW] `backend/main.py`
- FastAPI application with CORS, middleware, exception handlers
- Auto-generated Swagger/OpenAPI docs at `/docs`

#### [NEW] `backend/database.py`
- SQLAlchemy async engine + session management
- Alembic integration for migrations

#### [NEW] `backend/models/` (all ORM models)
- SQLAlchemy models mapping to all database tables

#### [NEW] `backend/schemas/` (all Pydantic schemas)
- Request/response schemas with validation

#### [NEW] `backend/routers/` (all route handlers)
- `auth.py` — login, register, refresh tokens
- `employees.py` — CRUD for employees
- `meals.py` — menus, meal types, transactions
- `predictions.py` — trigger predictions, get results
- `chatbot.py` — chat endpoint with streaming
- `reports.py` — generate/download reports
- `recommendations.py` — get AI recommendations
- `dashboard.py` — KPI aggregation endpoints
- `admin.py` — system administration

#### [NEW] `backend/auth/`
- JWT token generation/validation
- Role-based access control (Admin, Manager, Kitchen Staff, Viewer)
- Rate limiting middleware
- Audit logging middleware

#### [NEW] `backend/nlp/`
- LangChain RAG pipeline:
  - `chain.py` — Main conversational chain with memory
  - `tools.py` — Custom tools for querying predictions, database, generating reports
  - `prompts.py` — System prompts and few-shot examples
  - `vectorstore.py` — FAISS/ChromaDB for document retrieval
- The chatbot uses function calling to query the prediction engine, database, and report generator

#### [NEW] `backend/services/report_generator.py`
- Daily/Weekly/Monthly/Executive report generation
- Export as PDF (ReportLab) and Excel (openpyxl)
- Automated scheduling via APScheduler

#### [NEW] `backend/utils/cache.py`
- Redis caching layer for predictions, dashboard KPIs

---

### Batch 4: Frontend (Phase 9, 12)
*Next.js Dashboard & UI*

#### [NEW] `frontend/` (complete Next.js application)
- **Dashboard page** — Real-time KPIs (predicted vs actual meals, waste %, accuracy, cost savings, carbon footprint), trend charts, forecast visualization
- **Predictions page** — Tomorrow's prediction with confidence scores, per-meal-type breakdown, location/department drill-down, SHAP explanation cards
- **Reports page** — Generate & download daily/weekly/monthly reports, report history table
- **Employees page** — Employee directory with search/filter, department/location breakdown
- **Menus page** — Daily menu management, meal popularity analytics
- **Analytics page** — Deep-dive charts: demand trends, waste analysis, department comparison, seasonal patterns
- **Chatbot page** — Full-screen AI chat interface with streaming responses, suggested questions, rich card responses
- **Settings page** — System configuration, model retraining triggers, notification preferences
- **Admin page** — User management, role assignment, audit logs, system health

#### UI Design
- Dark theme with premium glassmorphism aesthetic
- Inter/Outfit fonts from Google Fonts
- Smooth micro-animations (Framer Motion)
- Recharts for data visualization
- Responsive (mobile-first)
- Color palette: Deep navy (#0a0e27), electric blue accents (#3b82f6), emerald green for positive (#10b981), amber for warnings (#f59e0b), rose for alerts (#f43f5e)

---

### Batch 5: DevOps, Testing & Documentation (Phases 14–18)
*Testing, Docker, CI/CD, Deployment Config, Final Documentation*

#### [NEW] `backend/tests/` (all test files)
- Unit tests for services, models, utilities
- Integration tests for API endpoints
- ML validation tests (model accuracy thresholds)
- Load tests with Locust

#### [NEW] `docker/` & `docker-compose.yml`
- Multi-stage Dockerfiles (backend, frontend, ML worker)
- Docker Compose orchestrating: PostgreSQL, Redis, FastAPI, Next.js, Nginx
- Development and production compose variants

#### [NEW] `.github/workflows/`
- CI pipeline: lint, test, build
- CD pipeline: Docker build + push, deploy to Azure

#### [NEW] `monitoring/`
- Prometheus scrape config for FastAPI metrics
- Grafana dashboard JSON for system monitoring

#### [NEW/UPDATE] `docs/` (all documentation)
- Complete SRS, SDD, Architecture Document
- API documentation (auto-generated from Swagger + manual enrichment)
- Deployment guide, User manual, Admin guide
- AI model documentation, Installation guide
- Maintenance guide, Future improvements

#### [NEW] `README.md`
- Professional project README with badges, setup instructions, screenshots

---

## Technology Decisions

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Backend | FastAPI (Python 3.11+) | Async, auto-docs, type-safe, as specified |
| Frontend | Next.js 14 (App Router) | SSR, RSC, as specified |
| Database | PostgreSQL 16 | Robust, as specified |
| ORM | SQLAlchemy 2.0 (async) | As specified, modern async support |
| ML | XGBoost, LightGBM, CatBoost, sklearn | Best gradient boosting libraries |
| Deep Learning | PyTorch | LSTM/Transformer forecasting |
| NLP | LangChain + OpenAI API | RAG chatbot as specified |
| Vector DB | ChromaDB | Simpler than FAISS for local dev |
| Cache | Redis | As specified |
| Charts | Recharts | React-native, performant |
| Animation | Framer Motion | Smooth UI animations |
| PDF Reports | ReportLab + Jinja2 | Professional PDF generation |
| Testing | pytest + httpx + Locust | Comprehensive test coverage |
| Containers | Docker + Compose | As specified |
| CI/CD | GitHub Actions | As specified |
| Monitoring | Prometheus + Grafana | As specified |

---

## Verification Plan

### Automated Tests
- `pytest backend/tests/` — Unit + integration tests (target 80%+ coverage)
- `pytest ml/tests/` — ML pipeline validation (R² > 0.85, MAPE < 15%)
- API tests via httpx test client against all endpoints
- Load test: 100 concurrent users on prediction endpoint

### Manual Verification
- Run `docker-compose up` and verify all services start
- Open frontend at `http://localhost:3000` and walk through all pages
- Test chatbot with sample questions from the requirements
- Generate a daily report and verify PDF output
- Trigger a prediction and verify SHAP explanations
- Browser recording of the full user flow

### Build Verification
- `npm run build` for frontend (no errors)
- `python -m pytest` for backend (all pass)
- `docker-compose build` (all images build successfully)
