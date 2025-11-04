# Oral Anti-Obesity Medication (AOM) Screening Application

A clinical decision support system for screening and recommending oral anti-obesity medications based on patient questionnaires and medical criteria.

## Overview

This application helps doctors make informed decisions about anti-obesity medication prescriptions by:
1. Collecting patient information through a digital questionnaire
2. Running a 4-step screening algorithm to determine eligible medications
3. Providing prioritized medication recommendations based on patient symptoms
4. Enabling doctors to review and make final medication selections

## Technology Stack

### Backend
- **Python 3.11+**
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - ORM for database interactions
- **PostgreSQL** - Primary database
- **Pydantic** - Data validation

### Frontend (To be implemented)
- **React 18** with TypeScript
- **Vite** - Build tool
- **TailwindCSS** - Styling

## Project Structure

```
aom-screening-app/
├── backend/
│   ├── app/
│   │   ├── api/              # API endpoints (to be created)
│   │   ├── core/             # Core configuration
│   │   │   └── config.py     # App settings
│   │   ├── db/               # Database setup
│   │   │   └── session.py    # DB connection
│   │   ├── models/           # SQLAlchemy models
│   │   │   ├── user.py
│   │   │   ├── questionnaire.py
│   │   │   └── screening_result.py
│   │   ├── schemas/          # Pydantic schemas (to be created)
│   │   ├── services/         # Business logic
│   │   │   └── screening_service.py  # Core screening algorithm
│   │   └── main.py           # FastAPI application
│   ├── requirements.txt
│   └── .env.example
├── frontend/                 # (To be created)
├── docs/
└── README.md
```

## Screening Algorithm

The application implements a 4-step screening mechanism:

### Step I: Eligibility Verification
- Medical evaluation completed
- Lifestyle modifications attempted (≥1 month)
- Contraception for women of childbearing age
- Bariatric surgery status assessment

### Step II: BMI-Based Determination
- BMI < 27: Not eligible
- BMI 27-29.9: Eligible with comorbidities
- BMI 30+: Eligible regardless of comorbidities

### Step III: Contraindication Screening
Excludes medications based on:
- Uncontrolled hypertension
- Kidney stones / Pregnancy plans
- Current medications (e.g., Tamoxifen)
- ADD/ADHD treatment
- Glaucoma status
- Cardiovascular conditions
- Psychiatric disorders
- Substance abuse history
- Thyroid dysfunction

### Step IV: Symptom-Based Prioritization
Prioritizes medications based on:
- Appetite control needs
- Behavioral eating patterns
- Binge eating disorder
- Emotional/night eating
- General weight loss goals

## Available Medications

- Phentermine
- Qsymia (Phentermine/Topiramate)
- Contrave (Naltrexone/Bupropion)
- Saxenda (Liraglutide)
- Wegovy (Semaglutide)
- Zepbound (Tirzepatide)
- Orlistat (last resort option)

## Database Schema

### Tables
1. **users** - Patients and doctors
2. **questionnaires** - Patient responses
3. **screening_results** - Medication recommendations

## Setup Instructions

### Prerequisites
- Python 3.11+
- PostgreSQL 14+
- Node.js 18+ (for frontend)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd aom-screening-app/backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

5. **Create PostgreSQL database:**
   ```bash
   createdb aom_screening_db
   ```

6. **Run the application:**
   ```bash
   uvicorn app.main:app --reload
   ```

7. **Access the API:**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs

## API Endpoints (To Be Implemented)

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

### Questionnaires
- `POST /api/questionnaires` - Create questionnaire
- `GET /api/questionnaires/{id}` - Get questionnaire
- `PUT /api/questionnaires/{id}` - Update questionnaire
- `POST /api/questionnaires/{id}/submit` - Submit for screening

### Screening
- `POST /api/screening/run` - Run screening algorithm
- `GET /api/screening/results/{id}` - Get screening results

### Doctor Dashboard
- `GET /api/doctor/pending` - Get pending questionnaires
- `POST /api/doctor/approve/{id}` - Approve medication selection

## Development Roadmap

- [x] Project structure setup
- [x] Database models
- [x] Core screening algorithm
- [ ] API endpoints
- [ ] Authentication system
- [ ] Frontend application
- [ ] Doctor dashboard
- [ ] Patient questionnaire form
- [ ] HIPAA compliance features
- [ ] Audit logging
- [ ] Testing suite
- [ ] Deployment configuration

## HIPAA Compliance Considerations

This application handles Protected Health Information (PHI) and must comply with HIPAA:

1. **Encryption**: All data encrypted at rest and in transit
2. **Access Control**: Role-based access (Patient/Doctor/Admin)
3. **Audit Logging**: Track all PHI access
4. **Authentication**: Secure password hashing with bcrypt
5. **Session Management**: Secure JWT tokens
6. **Business Associate Agreements**: Required for cloud hosting

## License

Proprietary - All rights reserved

## Contact

For questions or support, contact: [Your Contact Information]
