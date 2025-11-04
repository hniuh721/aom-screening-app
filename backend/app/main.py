from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import engine, Base

# Import models to register them with SQLAlchemy
from app.models import User, Questionnaire, ScreeningResult

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Oral Anti-Obesity Medications Screening Application"
)

# Configure CORS
# For production, allow Vercel domains
allowed_origins = settings.allowed_origins_list
# Add regex pattern for Vercel apps if in production
if settings.ENVIRONMENT == "production":
    allowed_origins = ["*"]  # Will be restricted by Render's built-in CORS later

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to AOM Screening Application API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# Include API routers
from app.api import auth, questionnaires, screening

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(questionnaires.router, prefix="/api/questionnaires", tags=["Questionnaires"])
app.include_router(screening.router, prefix="/api/screening", tags=["Screening"])
