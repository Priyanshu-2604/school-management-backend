# 🏫 School Management System Backend

A modular **FastAPI** backend application for managing school operations, student analytics, ML-based predictions, and voice command interpretation.

---

## 🚀 Features

- 🔐 JWT Authentication & Role-Based Access Control
- 📊 Transaction & Revenue Reporting
- 📚 Student Performance and Attendance Analytics
- 👨‍🏫 Teacher Effectiveness Evaluation
- 🤖 ML Models for Performance, Dropout, and Revenue Predictions
- 🎙️ Voice Command Parser for Natural Language Queries

---

## 🗂️ Project Structure

school_management_backend/
│
├── app/
│   ├── __init__.py
│   ├── main.py                       # FastAPI entry point (includes /health)
│
│   ├── core/                         # Core logic: settings, security, auth, logging
│   │   ├── __init__.py
│   │   ├── config.py                 # Loads .env configs
│   │   ├── auth.py                   # JWT authentication
│   │   ├── security.py               # Token creation & password utils
│   │   └── logger.py                 # Structured logging setup
│
│   ├── db/                           # Database layer
│   │   ├── __init__.py
│   │   ├── base.py                   # SQLAlchemy base
│   │   ├── models.py                 # All DB models
│   │   ├── session.py                # DB session maker
│   │   └── seed.py                   # Optional data seed script
│
│   ├── schemas/                      # Pydantic models for request/response
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── student.py
│   │   ├── transaction.py
│   │   └── report.py
│
│   ├── services/                     # Business logic, ML, NLP
│   │   ├── __init__.py
│   │   ├── ml_models.py              # Predict performance, dropout, revenue
│   │   └── voice_parser.py           # Parse voice commands using spaCy
│
│   ├── api/                          # API routes
│   │   ├── __init__.py
│   │   ├── dependencies.py           # Reusable FastAPI dependencies
│   │   ├── auth.py                   # /auth/login, /auth/register
│   │   ├── transactions.py           # /transactions/report
│   │   ├── students.py               # /students/performance, /student/overview
│   │   ├── teachers.py               # /teachers/effectiveness
│   │   ├── management.py             # /management/kpis
│   │   └── voice.py                  # /voice/interpret
│
├── models/                           # Pre-trained ML models (.pkl, Prophet, etc.)
│   ├── student_performance_model.pkl
│   ├── dropout_risk_model.pkl
│   └── revenue_forecast_model.pkl
│
├── tests/                            # Unit tests (pytest)
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_students.py
│   ├── test_ml_models.py
│   └── test_voice.py
│
├── Dockerfile                        # Docker build for FastAPI app
├── docker-compose.yml                # Compose file for API + DB + Redis + Nginx
├── init.sql                          # Optional DB init script (tables, seed data)
├── nginx.conf                        # Optional Nginx reverse proxy
├── .env                              # Environment variables (not committed to Git)
├── .env.template                     # Sample .env to share
├── requirements.txt                  # All Python dependencies
├── README.md                         # Project documentation
└── alembic.ini                       # Optional: Alembic for DB migrations



---

## ⚙️ Setup Instructions

1. **Clone the repository**
git clone https://github.com/your-username/school-backend.git
cd school-backend
Install dependencies

2. **Install the Dependencies**
pip install -r requirements.txt

3. **Set up environment variables**
Create a .env file with:
SECRET_KEY=your-secret-key
ALGORITHM=HS256

4. **Run the app**
uvicorn app.main:app --reload

5. **Seed the database (Optional)**
python app/db/seed.py


📌 API Documentation
Interactive docs: http://localhost:8000/docs
Authenticate via /auth/login to get a bearer token for protected routes.


🔑 Sample Users (for testing)
Username	Password	Role
admin	admin123	admin
teacher1	teach123	teacher


🔍 Key Endpoints
/auth/register, /auth/login
/transactions/report
/students/performance
/predict/performance, /predict/dropout, /predict/revenue
/management/kpis
/voice/interpret
