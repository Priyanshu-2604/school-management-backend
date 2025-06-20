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

school_backend/
│
├── app/
│ ├── api/ # Route handlers
│ ├── core/ # Config, security, logger
│ ├── db/ # Database models, session, seed
│ ├── schemas/ # Pydantic models
│ ├── services/ # ML models & voice parser logic
│ └── main.py # FastAPI app entry point
│
├── requirements.txt
└── README.md


---

## ⚙️ Setup Instructions

1. **Clone the repository**
```bash
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
