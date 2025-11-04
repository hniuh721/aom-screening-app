from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.user import User
from app.models.questionnaire import Questionnaire, QuestionnaireStatus
from app.models.screening_result import ScreeningResult
from app.schemas.screening import ScreeningResultResponse, DoctorApproval
from app.core.deps import get_current_user, get_current_active_doctor
from app.services.screening_service import ScreeningService
from datetime import datetime

router = APIRouter()


@router.post("/run/{questionnaire_id}", response_model=ScreeningResultResponse, status_code=status.HTTP_201_CREATED)
def run_screening(
    questionnaire_id: int,
    db: Session = Depends(get_db)
):
    """
    Run screening algorithm on a submitted questionnaire (public access - no authentication required)

    This endpoint executes the 4-step screening algorithm and returns medication recommendations
    """
    # Get questionnaire
    questionnaire = db.query(Questionnaire).filter(Questionnaire.id == questionnaire_id).first()

    if not questionnaire:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Questionnaire not found"
        )

    # Check if questionnaire is submitted
    if questionnaire.status != QuestionnaireStatus.SUBMITTED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Questionnaire must be submitted before screening"
        )

    # Check if screening already exists
    existing_result = db.query(ScreeningResult).filter(
        ScreeningResult.questionnaire_id == questionnaire_id
    ).first()

    if existing_result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Screening already performed for this questionnaire"
        )

    # Prepare questionnaire data for screening
    questionnaire_data = {
        "age": questionnaire.age,
        "gender": questionnaire.gender,
        "is_childbearing_age_woman": questionnaire.is_childbearing_age_woman,
        "has_medical_evaluation": questionnaire.has_medical_evaluation,
        "attempted_lifestyle_modifications": questionnaire.attempted_lifestyle_modifications,
        "has_reliable_contraception": questionnaire.has_reliable_contraception,
        "bariatric_surgery_status": questionnaire.bariatric_surgery_status,
        "height_ft": questionnaire.height_ft,
        "height_in": questionnaire.height_in,
        "weight_lb": questionnaire.weight_lb,
        "comorbidities": questionnaire.comorbidities or [],
        "symptoms": questionnaire.symptoms or [],
        "health_conditions": questionnaire.health_conditions or [],
    }

    # Run screening algorithm
    screener = ScreeningService()
    screening_result = screener.run_screening(questionnaire_data)

    # Save screening result to database
    db_result = ScreeningResult(
        questionnaire_id=questionnaire.id,
        patient_id=questionnaire.patient_id,
        is_eligible=screening_result["is_eligible"],
        eligibility_message=screening_result["eligibility_message"],
        bmi_category=screening_result["bmi_category"],
        initial_drug_pool=[str(drug) for drug in screening_result["initial_drug_pool"]],
        excluded_drugs={str(k): v for k, v in screening_result["excluded_drugs"].items()},
        recommended_drugs=screening_result["recommended_drugs"],
        screening_logic=screening_result["screening_steps"],
        warnings=screening_result["warnings"],
    )

    db.add(db_result)
    db.commit()
    db.refresh(db_result)

    return db_result


@router.get("/results/{questionnaire_id}", response_model=ScreeningResultResponse)
def get_screening_result(
    questionnaire_id: int,
    db: Session = Depends(get_db)
):
    """
    Get screening results for a questionnaire (public access - no authentication required)
    """
    # Get screening result
    result = db.query(ScreeningResult).filter(
        ScreeningResult.questionnaire_id == questionnaire_id
    ).first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Screening result not found"
        )

    return result


@router.get("/pending", response_model=List[ScreeningResultResponse])
def get_pending_screenings(
    current_user: User = Depends(get_current_active_doctor),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Get all pending screening results (doctors only)

    Returns screening results that haven't been approved by a doctor yet
    """
    results = db.query(ScreeningResult).filter(
        ScreeningResult.doctor_selected_medication.is_(None)
    ).offset(skip).limit(limit).all()

    return results


@router.post("/approve/{screening_id}", response_model=ScreeningResultResponse)
def approve_medication(
    screening_id: int,
    approval: DoctorApproval,
    current_user: User = Depends(get_current_active_doctor),
    db: Session = Depends(get_db)
):
    """
    Doctor approves a medication selection (doctors only)

    Doctor reviews the screening recommendations and makes final medication selection
    """
    result = db.query(ScreeningResult).filter(ScreeningResult.id == screening_id).first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Screening result not found"
        )

    # Update with doctor's selection
    result.doctor_selected_medication = approval.selected_medication
    result.doctor_notes = approval.notes
    result.doctor_approved_at = datetime.utcnow()

    # Update questionnaire status
    questionnaire = db.query(Questionnaire).filter(
        Questionnaire.id == result.questionnaire_id
    ).first()

    if questionnaire:
        questionnaire.status = QuestionnaireStatus.REVIEWED
        questionnaire.reviewed_at = datetime.utcnow()
        questionnaire.reviewed_by_doctor_id = current_user.id

    db.commit()
    db.refresh(result)

    return result
