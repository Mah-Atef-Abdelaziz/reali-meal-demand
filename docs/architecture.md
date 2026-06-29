# System Architecture Document
# AI Meal Demand Prediction & Smart Assistant

**Version:** 1.0 | **Date:** 2026-06-29

## High-Level Architecture

Microservices-oriented monolith with Docker Compose orchestration.

### Components
- **Frontend:** Next.js 14 (App Router) — Port 3000
- **Backend:** FastAPI (Python 3.11+) — Port 8000
- **Database:** PostgreSQL 16 — Port 5432
- **Cache:** Redis 7 — Port 6379
- **Vector DB:** ChromaDB — Port 8100
- **Monitoring:** Prometheus (9090) + Grafana (3001)
- **Proxy:** Nginx (80/443)

## Backend Architecture (FastAPI)
- `main.py` — App entry, middleware, CORS
- `config.py` — Pydantic Settings (env-based)
- `database.py` — SQLAlchemy async engine
- `auth/` — JWT, RBAC, rate limiting
- `models/` — SQLAlchemy ORM (18+ tables)
- `schemas/` — Pydantic request/response
- `routers/` — REST API handlers
- `services/` — Business logic (prediction, chatbot, reports, recommendations)
- `nlp/` — LangChain RAG pipeline
- `utils/` — Redis cache, structured logging

## Frontend Architecture (Next.js 14)
- App Router with 10 pages: Dashboard, Predictions, Reports, Employees, Menus, Analytics, Chatbot, Settings, Admin, Login
- Recharts for visualization, Framer Motion for animations
- REAL.i brand: gold (#D4AF37) / charcoal (#1a1a2e), Orbitron/Montserrat fonts

## ML Pipeline
- **Offline:** Data → Preprocess → Feature Engineering → Train (XGBoost/LightGBM/CatBoost/RF/LSTM) → Evaluate → SHAP → Save
- **Online:** API Request → Load Model → Predict → Explain → Cache → Return
- **Features:** temporal, historical lags, menu, weather, employee, location, events (50+)

## NLP Pipeline
- LangChain Agent with custom tools (query_predictions, query_database, generate_report, explain_prediction)
- RAG via ChromaDB for knowledge base retrieval
- OpenAI GPT (primary) with Ollama fallback
- Conversation memory (window k=10)

## Security
- JWT authentication with refresh tokens
- 4 roles: Admin, Manager, Kitchen Staff, Viewer
- Rate limiting, audit logging, input validation, HTTPS

## Deployment
- Docker Compose for local development
- Azure Container Apps (free tier) for production
- GitHub Actions CI/CD
