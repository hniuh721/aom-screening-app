# Frontend Setup Guide

## 🔧 Fix NPM Permission Issue First

Before running the frontend, fix the npm cache permission issue:

```bash
# In your terminal (not Claude Code), run:
sudo chown -R $(whoami) ~/.npm
```

Then install dependencies:

```bash
cd /Users/yawenwang/aom-screening-app/frontend
npm install
```

## 🚀 Run Frontend

After npm install completes:

```bash
npm run dev
```

The frontend will start at: **http://localhost:5173**

## 📦 Dependencies Added

The package.json includes:
- **react-router-dom** - Routing
- **axios** - API calls
- **react-hook-form** - Form validation

## 🎯 What's Included

### Pages:
1. **Login** - `/login`
2. **Register** - `/register`
3. **Questionnaire** - `/questionnaire` (patients)
4. **Dashboard** - `/dashboard` (doctors)
5. **Results** - `/results/:id`

### Features:
- JWT authentication
- Role-based routing (patient/doctor)
- Multi-step questionnaire form
- Screening results display
- Doctor approval interface

## 🔗 API Configuration

The frontend connects to backend at:
- **Backend URL**: `http://localhost:8000`
- **API Base**: `http://localhost:8000/api`

Both servers run simultaneously:
- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:5173

## 📋 Test Workflow

### As a Patient:
1. Register at `/register` with role="patient"
2. Login
3. Fill questionnaire
4. Submit for screening
5. View recommendations

### As a Doctor:
1. Register with role="doctor"
2. Login
3. View pending questionnaires
4. Review recommendations
5. Approve medication

## 🐛 Troubleshooting

### Port already in use:
```bash
# Kill process on port 5173
lsof -ti:5173 | xargs kill
```

### Cannot connect to API:
- Ensure backend is running on port 8000
- Check CORS settings in backend

### Build errors:
```bash
# Clean install
rm -rf node_modules package-lock.json
npm install
```

## 📁 Project Structure

```
frontend/src/
├── api/                  # API service
│   └── client.ts
├── context/             # React context
│   └── AuthContext.tsx
├── pages/               # Page components
│   ├── Login.tsx
│   ├── Register.tsx
│   ├── Questionnaire.tsx
│   ├── Dashboard.tsx
│   └── Results.tsx
├── components/          # Reusable components
│   └── ...
├── App.tsx             # Main app with routing
└── main.tsx            # Entry point
```

## ⚡ Quick Start (After npm install)

```bash
# Terminal 1: Backend (already running)
cd backend
./venv/bin/uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev
```

Then open http://localhost:5173 in your browser!
