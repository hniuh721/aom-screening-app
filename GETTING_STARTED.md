# Getting Started with AOM Screening Application

## Quick Start Guide

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11+**: [Download Python](https://www.python.org/downloads/)
- **PostgreSQL 14+**: [Download PostgreSQL](https://www.postgresql.org/download/)
- **Git**: [Download Git](https://git-scm.com/downloads)

### Step 1: Navigate to Project Directory

```bash
cd /Users/yawenwang/aom-screening-app
```

### Step 2: Set Up Backend

#### Option A: Automatic Setup (Recommended)

```bash
cd backend
./setup.sh
```

#### Option B: Manual Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
```

### Step 3: Configure Database

1. **Create PostgreSQL database:**

```bash
createdb aom_screening_db
```

2. **Edit `.env` file** in the `backend` directory:

```env
DATABASE_URL=postgresql://YOUR_USERNAME:YOUR_PASSWORD@localhost:5432/aom_screening_db
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
ENVIRONMENT=development
```

Replace `YOUR_USERNAME` and `YOUR_PASSWORD` with your PostgreSQL credentials.

### Step 4: Test the Screening Algorithm

Before running the full application, test the core screening logic:

```bash
cd backend
source venv/bin/activate  # If not already activated
python test_screening.py
```

You should see detailed output showing how the screening algorithm works with different patient scenarios.

### Step 5: Run the Backend Server

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

The server will start at: **http://localhost:8000**

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Step 6: Verify Installation

Open your browser and visit:
- http://localhost:8000 - Should show welcome message
- http://localhost:8000/docs - Interactive API documentation

## Project Structure Overview

```
aom-screening-app/
├── backend/
│   ├── app/
│   │   ├── core/              # Configuration
│   │   ├── db/                # Database setup
│   │   ├── models/            # Data models
│   │   ├── services/          # Business logic
│   │   │   └── screening_service.py  # ⭐ Core algorithm
│   │   └── main.py            # FastAPI app
│   ├── requirements.txt
│   ├── .env.example
│   ├── setup.sh
│   └── test_screening.py      # Algorithm tests
└── README.md
```

## Understanding the Screening Algorithm

The application implements a **4-step screening process**:

### Step I: Eligibility Verification
✅ Checks if patient meets basic criteria:
- Medical evaluation completed
- Lifestyle modifications attempted
- Contraception (for women of childbearing age)
- Bariatric surgery status

### Step II: BMI-Based Determination
📊 Determines eligibility based on BMI:
- BMI 27-29.9: Requires ≥1 comorbidity
- BMI 30+: Eligible regardless

### Step III: Contraindication Screening
❌ Excludes unsafe medications based on:
- Health conditions
- Current medications
- Medical history

### Step IV: Symptom-Based Prioritization
🎯 Ranks medications by patient symptoms:
- Appetite control
- Behavioral eating patterns
- Binge eating disorder
- Weight loss goals

## Next Steps

### For Development:

1. **Create API Endpoints** - Build REST APIs for questionnaires and screening
2. **Add Authentication** - Implement user login/registration
3. **Build Frontend** - Create React application
4. **Add Testing** - Write unit and integration tests

### For Testing:

Run the test script to see the algorithm in action:

```bash
python backend/test_screening.py
```

This demonstrates 3 patient scenarios:
1. ✅ Eligible patient with recommendations
2. ❌ Ineligible (low BMI without comorbidities)
3. ⚠️  Patient with contraindications

## Common Issues

### Database Connection Error

**Error**: `could not connect to server`

**Solution**: Ensure PostgreSQL is running:
```bash
# macOS
brew services start postgresql

# Linux
sudo service postgresql start

# Windows
# Start PostgreSQL service from Services panel
```

### Import Errors

**Error**: `ModuleNotFoundError`

**Solution**: Ensure virtual environment is activated:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Port Already in Use

**Error**: `Address already in use`

**Solution**: Change port or kill existing process:
```bash
# Run on different port
uvicorn app.main:app --reload --port 8001

# Or find and kill process using port 8000
lsof -ti:8000 | xargs kill
```

## Development Workflow

1. **Make changes** to code
2. **Test** with `test_screening.py`
3. **Run server** with `--reload` flag (auto-reloads on changes)
4. **Test endpoints** at http://localhost:8000/docs
5. **Commit changes** to git

## Need Help?

- Check the main [README.md](README.md) for detailed documentation
- Review API docs at http://localhost:8000/docs
- Examine `test_screening.py` for usage examples

## What's Been Built So Far

✅ **Completed:**
- Project structure
- Database models (User, Questionnaire, ScreeningResult)
- Core screening algorithm (4-step process)
- Configuration management
- Test suite

⏳ **Coming Next:**
- API endpoints
- Authentication system
- Frontend application
- Doctor dashboard
- Patient questionnaire form

---

**Ready to build the rest of the application?**

You now have a solid foundation! The core screening logic is complete and tested. Next, we'll build the API endpoints and frontend interface.
