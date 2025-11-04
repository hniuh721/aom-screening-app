from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class MedicationRecommendation(BaseModel):
    """Individual medication recommendation"""
    medication: str
    priority: int
    reasoning: str


class ScreeningResultResponse(BaseModel):
    """Complete screening result"""
    id: int
    questionnaire_id: int
    patient_id: Optional[int] = None  # Nullable for anonymous submissions
    is_eligible: bool
    eligibility_message: Optional[str] = None
    bmi_category: Optional[str] = None
    initial_drug_pool: Optional[List[str]] = []
    excluded_drugs: Optional[Dict[str, str]] = {}
    recommended_drugs: Optional[List[Dict[str, Any]]] = []
    screening_logic: Optional[List[Dict[str, str]]] = []
    warnings: Optional[List[str]] = []
    doctor_selected_medication: Optional[str] = None
    doctor_notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class DoctorApproval(BaseModel):
    """Schema for doctor to approve medication"""
    selected_medication: str
    notes: Optional[str] = None


class ScreeningRequest(BaseModel):
    """Request to run screening on a questionnaire"""
    questionnaire_id: int
