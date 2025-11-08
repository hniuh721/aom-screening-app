from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.db.session import Base


class QuestionnaireStatus(str, enum.Enum):
    """Questionnaire status"""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    REVIEWED = "reviewed"


class Questionnaire(Base):
    """Patient questionnaire responses"""
    __tablename__ = "questionnaires"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Nullable for anonymous submissions
    status = Column(SQLEnum(QuestionnaireStatus), default=QuestionnaireStatus.DRAFT)

    # Section I: Basic Information
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    contact_number = Column(String, nullable=True)
    is_childbearing_age_woman = Column(Boolean, nullable=True)
    height_ft = Column(Integer, nullable=False)
    height_in = Column(Integer, nullable=False)
    weight_lb = Column(Float, nullable=False)
    bmi = Column(Float, nullable=True)  # Calculated

    # Section II: Eating Habits & Feelings
    eating_habits = Column(JSON, nullable=True)  # List of eating habits

    # Section III: Medical Conditions & Health Status
    health_conditions = Column(JSON, nullable=True)  # List of health conditions

    # Section IV: Medication and Allergy History
    current_medications = Column(JSON, nullable=True)  # List of medications
    has_drug_allergies = Column(Boolean, nullable=False)
    drug_allergies = Column(JSON, nullable=True)  # List of allergies

    # Section V: Additional Remarks
    additional_remarks = Column(String, nullable=True)

    # Metadata
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    reviewed_by_doctor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships commented out to avoid SQLAlchemy ambiguous foreign key errors
    # Access related data using foreign key columns directly (patient_id, reviewed_by_doctor_id)
    # patient = relationship("User", foreign_keys=[patient_id])
    # reviewed_by = relationship("User", foreign_keys=[reviewed_by_doctor_id])
    # screening_result = relationship("ScreeningResult", foreign_keys="ScreeningResult.questionnaire_id", uselist=False)
