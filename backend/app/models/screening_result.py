from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base


class ScreeningResult(Base):
    """Screening results and medication recommendations"""
    __tablename__ = "screening_results"

    id = Column(Integer, primary_key=True, index=True)
    questionnaire_id = Column(Integer, ForeignKey("questionnaires.id"), unique=True, nullable=False)
    patient_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Nullable for anonymous submissions

    # Eligibility
    is_eligible = Column(Boolean, nullable=False)
    eligibility_message = Column(Text, nullable=True)

    # Patient demographic info
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    is_childbearing_age_woman = Column(Boolean, nullable=True)

    # Screening steps details
    bmi_category = Column(String, nullable=True)
    initial_drug_pool = Column(JSON, nullable=True)  # List of initial medications
    excluded_drugs = Column(JSON, nullable=True)  # Drugs excluded with reasons
    recommended_drugs = Column(JSON, nullable=True)  # Final recommended drugs with priority

    # Detailed reasoning for doctors
    screening_logic = Column(JSON, nullable=True)  # Step-by-step logic applied
    warnings = Column(JSON, nullable=True)  # Any warnings or special considerations

    # Doctor's final decision
    doctor_selected_medication = Column(String, nullable=True)
    doctor_notes = Column(Text, nullable=True)
    doctor_approved_at = Column(DateTime(timezone=True), nullable=True)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships commented out to avoid SQLAlchemy ambiguous foreign key errors
    # Access related data using foreign key columns directly (questionnaire_id, patient_id)
    # questionnaire = relationship("Questionnaire", foreign_keys=[questionnaire_id])
    # patient = relationship("User", foreign_keys=[patient_id])
