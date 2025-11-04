# AOM Screening API - Usage Guide

## 🚀 Server is Running!

Your FastAPI server is now live at: **http://localhost:8000**

## 📚 Interactive API Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔑 Available API Endpoints

### Authentication (`/api/auth`)

#### 1. Register New User
```
POST /api/auth/register
```
**Body:**
```json
{
  "email": "patient@example.com",
  "password": "securepassword123",
  "full_name": "John Doe",
  "role": "patient",
  "phone_number": "555-1234"
}
```

**Roles:** `patient` or `doctor`

#### 2. Login
```
POST /api/auth/login
```
**Form Data:**
- `username`: your email
- `password`: your password

**Response:**
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

#### 3. Get Current User
```
GET /api/auth/me
Authorization: Bearer {your_token}
```

---

### Questionnaires (`/api/questionnaires`)

#### 1. Create Questionnaire (Patient Only)
```
POST /api/questionnaires
Authorization: Bearer {patient_token}
```
**Body:**
```json
{
  "age": 35,
  "gender": "female",
  "contact_number": "555-1234",
  "is_childbearing_age_woman": true,
  "has_medical_evaluation": true,
  "attempted_lifestyle_modifications": true,
  "has_reliable_contraception": true,
  "bariatric_surgery_status": "not_applicable",
  "height_ft": 5,
  "height_in": 4,
  "weight_lb": 185,
  "comorbidities": ["hypertension", "type_2_diabetes"],
  "symptoms": ["excessive_appetite", "emotional_eating"],
  "health_conditions": ["controlled_hypertension"],
  "current_medications": [],
  "has_drug_allergies": false,
  "drug_allergies": [],
  "additional_remarks": ""
}
```

#### 2. List Questionnaires
```
GET /api/questionnaires
Authorization: Bearer {token}
```
- Patients: see only their own
- Doctors: see all

#### 3. Get Specific Questionnaire
```
GET /api/questionnaires/{id}
Authorization: Bearer {token}
```

#### 4. Update Questionnaire (Patient Only, Draft Only)
```
PUT /api/questionnaires/{id}
Authorization: Bearer {patient_token}
```

#### 5. Submit Questionnaire for Screening (Patient Only)
```
POST /api/questionnaires/{id}/submit
Authorization: Bearer {patient_token}
```

#### 6. Delete Questionnaire (Patient Only, Draft Only)
```
DELETE /api/questionnaires/{id}
Authorization: Bearer {patient_token}
```

---

### Screening (`/api/screening`)

#### 1. Run Screening Algorithm
```
POST /api/screening/run/{questionnaire_id}
Authorization: Bearer {token}
```

**This is the KEY endpoint!** It runs the 4-step screening algorithm.

**Response:**
```json
{
  "id": 1,
  "questionnaire_id": 1,
  "patient_id": 1,
  "is_eligible": true,
  "eligibility_message": "Patient meets all eligibility criteria",
  "bmi_category": "BMI 30-34.9 (Class 1 Obesity)",
  "initial_drug_pool": ["Phentermine", "Qsymia", "Contrave", ...],
  "excluded_drugs": {},
  "recommended_drugs": [
    {
      "medication": "Qsymia (Phentermine/Topiramate)",
      "priority": 1,
      "reasoning": "First-line: Balances appetite suppression + eating behavior"
    }
  ],
  "screening_logic": [...],
  "warnings": ["Blood pressure monitoring required"],
  "created_at": "2025-11-01T00:00:00"
}
```

#### 2. Get Screening Results
```
GET /api/screening/results/{questionnaire_id}
Authorization: Bearer {token}
```

#### 3. Get Pending Screenings (Doctors Only)
```
GET /api/screening/pending
Authorization: Bearer {doctor_token}
```

#### 4. Approve Medication (Doctors Only)
```
POST /api/screening/approve/{screening_id}
Authorization: Bearer {doctor_token}
```
**Body:**
```json
{
  "selected_medication": "Qsymia (Phentermine/Topiramate)",
  "notes": "Patient is suitable for this medication. Start with lowest dose."
}
```

---

## 🧪 Testing the Complete Workflow

### Step 1: Register a Patient
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "patient@test.com",
    "password": "test123",
    "full_name": "Jane Patient",
    "role": "patient",
    "phone_number": "555-1234"
  }'
```

### Step 2: Login as Patient
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=patient@test.com&password=test123"
```

**Save the access_token from response!**

### Step 3: Create Questionnaire
```bash
curl -X POST http://localhost:8000/api/questionnaires \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 35,
    "gender": "female",
    "is_childbearing_age_woman": true,
    "has_medical_evaluation": true,
    "attempted_lifestyle_modifications": true,
    "has_reliable_contraception": true,
    "bariatric_surgery_status": "not_applicable",
    "height_ft": 5,
    "height_in": 4,
    "weight_lb": 185,
    "comorbidities": ["hypertension"],
    "symptoms": ["excessive_appetite"],
    "health_conditions": ["controlled_hypertension"],
    "current_medications": [],
    "has_drug_allergies": false,
    "drug_allergies": []
  }'
```

**Save the questionnaire ID from response!**

### Step 4: Submit Questionnaire
```bash
curl -X POST http://localhost:8000/api/questionnaires/1/submit \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Step 5: Run Screening
```bash
curl -X POST http://localhost:8000/api/screening/run/1 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**This runs the algorithm and returns medication recommendations!**

---

## 🎯 Best Way to Test: Use Interactive Docs

1. **Open** http://localhost:8000/docs
2. **Click "Authorize"** button (top right)
3. **Login** to get token (use `/api/auth/login`)
4. **Copy token** and paste in Authorize dialog
5. **Try endpoints** directly from the browser!

---

## 📊 Example: Complete Patient Journey

1. **Patient registers** → Gets account
2. **Patient logs in** → Gets JWT token
3. **Patient fills questionnaire** → Saves as draft
4. **Patient updates** if needed → Still draft
5. **Patient submits** → Status: SUBMITTED
6. **Patient runs screening** → Gets recommendations
7. **Doctor views pending** → Sees patient's case
8. **Doctor approves medication** → Final selection made
9. **Patient status** → REVIEWED

---

## 🔒 Authentication

All protected endpoints require JWT token in header:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

Get token from `/api/auth/login` endpoint.

---

## 🗄️ Database

SQLite database created at:
```
/Users/yawenwang/aom-screening-app/backend/aom_screening.db
```

Tables:
- `users` - Patients and doctors
- `questionnaires` - Patient responses
- `screening_results` - Algorithm recommendations

---

## 🛑 Stop the Server

To stop the server, use:
```bash
# Find the process
lsof -ti:8000 | xargs kill

# Or press Ctrl+C in the terminal where it's running
```

---

## 🎉 What's Working

✅ User authentication (register/login)
✅ JWT token-based security
✅ Role-based access control (patient/doctor)
✅ Questionnaire CRUD operations
✅ BMI auto-calculation
✅ 4-step screening algorithm
✅ Medication recommendations
✅ Doctor approval workflow
✅ Database persistence
✅ Interactive API docs

---

## 🚀 Next Steps

1. **Build Frontend** - React app for patient questionnaire form
2. **Doctor Dashboard** - Review and approve medications
3. **Email Notifications** - Notify doctors of new submissions
4. **Export Results** - PDF reports
5. **Production Deploy** - AWS/Heroku with PostgreSQL
6. **HIPAA Compliance** - Encryption, audit logs

---

**Your API is fully functional and ready to use!** 🎊
