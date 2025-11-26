from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
from app.models.questionnaire import QuestionnaireStatus


class QuestionnaireBase(BaseModel):
    """Base questionnaire schema - matches new 5-section format"""
    # Section I: Basic Information
    height_ft: int
    height_in: int
    weight_lb: float

    # Section II: Eating Habits & Feelings
    eating_habits: Optional[List[str]] = []

    # Section III: Medical Conditions & Health Status
    health_conditions: Optional[List[str]] = []
    condition_control_status: Optional[Dict[str, str]] = None  # Maps condition key to "controlled"/"uncontrolled"
    previous_aom_history: Optional[str] = None

    # Section IV: Medication and Allergy History
    current_medications: Optional[List[str]] = []
    has_drug_allergies: bool
    drug_allergies: Optional[List[str]] = []

    # Section V: Additional Remarks
    additional_remarks: Optional[str] = None


class QuestionnaireCreate(QuestionnaireBase):
    """Schema for creating a questionnaire"""
    age: int
    gender: str
    contact_number: Optional[str] = None
    is_childbearing_age_woman: Optional[bool] = None


class QuestionnaireUpdate(BaseModel):
    """Schema for updating a questionnaire"""
    height_ft: Optional[int] = None
    height_in: Optional[int] = None
    weight_lb: Optional[float] = None
    eating_habits: Optional[List[str]] = None
    health_conditions: Optional[List[str]] = None
    condition_control_status: Optional[Dict[str, str]] = None
    previous_aom_history: Optional[str] = None
    current_medications: Optional[List[str]] = None
    has_drug_allergies: Optional[bool] = None
    drug_allergies: Optional[List[str]] = None
    additional_remarks: Optional[str] = None


class QuestionnaireResponse(QuestionnaireBase):
    """Schema for questionnaire response"""
    id: int
    patient_id: Optional[int] = None  # Nullable for anonymous submissions
    status: QuestionnaireStatus
    age: int
    gender: str
    contact_number: Optional[str] = None
    is_childbearing_age_woman: Optional[bool] = None
    bmi: Optional[float] = None
    submitted_at: Optional[datetime] = None
    reviewed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class QuestionnaireListResponse(BaseModel):
    """Schema for listing questionnaires"""
    id: int
    patient_id: int
    status: QuestionnaireStatus
    bmi: Optional[float] = None
    submitted_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True
