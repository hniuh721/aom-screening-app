from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.db.session import get_db
from app.models.user import User
from app.models.questionnaire import Questionnaire, QuestionnaireStatus
from app.schemas.questionnaire import (
    QuestionnaireCreate,
    QuestionnaireUpdate,
    QuestionnaireResponse,
    QuestionnaireListResponse,
)
from app.core.deps import get_current_user, get_current_active_patient
from app.services.screening_service import ScreeningService

router = APIRouter()


@router.post("/anonymous", response_model=QuestionnaireResponse, status_code=status.HTTP_201_CREATED)
def create_anonymous_questionnaire(
    questionnaire_data: QuestionnaireCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new questionnaire without authentication (public access)

    Saves the questionnaire as a draft that can be submitted immediately
    """
    # Calculate BMI
    screener = ScreeningService()
    bmi = screener.calculate_bmi(
        questionnaire_data.height_ft,
        questionnaire_data.height_in,
        questionnaire_data.weight_lb
    )

    # Create questionnaire without patient_id (anonymous)
    db_questionnaire = Questionnaire(
        patient_id=None,  # Anonymous submission
        status=QuestionnaireStatus.DRAFT,
        age=questionnaire_data.age,
        gender=questionnaire_data.gender,
        contact_number=questionnaire_data.contact_number,
        is_childbearing_age_woman=questionnaire_data.is_childbearing_age_woman,
        height_ft=questionnaire_data.height_ft,
        height_in=questionnaire_data.height_in,
        weight_lb=questionnaire_data.weight_lb,
        bmi=bmi,
        eating_habits=questionnaire_data.eating_habits,
        health_conditions=questionnaire_data.health_conditions,
        current_medications=questionnaire_data.current_medications,
        has_drug_allergies=questionnaire_data.has_drug_allergies,
        drug_allergies=questionnaire_data.drug_allergies,
        additional_remarks=questionnaire_data.additional_remarks,
    )

    db.add(db_questionnaire)
    db.commit()
    db.refresh(db_questionnaire)

    return db_questionnaire


@router.post("", response_model=QuestionnaireResponse, status_code=status.HTTP_201_CREATED)
def create_questionnaire(
    questionnaire_data: QuestionnaireCreate,
    current_user: User = Depends(get_current_active_patient),
    db: Session = Depends(get_db)
):
    """
    Create a new questionnaire (patients only)

    Saves the questionnaire as a draft that can be updated later
    """
    # Calculate BMI
    screener = ScreeningService()
    bmi = screener.calculate_bmi(
        questionnaire_data.height_ft,
        questionnaire_data.height_in,
        questionnaire_data.weight_lb
    )

    # Create questionnaire
    db_questionnaire = Questionnaire(
        patient_id=current_user.id,
        status=QuestionnaireStatus.DRAFT,
        age=questionnaire_data.age,
        gender=questionnaire_data.gender,
        contact_number=questionnaire_data.contact_number,
        is_childbearing_age_woman=questionnaire_data.is_childbearing_age_woman,
        height_ft=questionnaire_data.height_ft,
        height_in=questionnaire_data.height_in,
        weight_lb=questionnaire_data.weight_lb,
        bmi=bmi,
        eating_habits=questionnaire_data.eating_habits,
        health_conditions=questionnaire_data.health_conditions,
        current_medications=questionnaire_data.current_medications,
        has_drug_allergies=questionnaire_data.has_drug_allergies,
        drug_allergies=questionnaire_data.drug_allergies,
        additional_remarks=questionnaire_data.additional_remarks,
    )

    db.add(db_questionnaire)
    db.commit()
    db.refresh(db_questionnaire)

    return db_questionnaire


@router.get("", response_model=List[QuestionnaireListResponse])
def list_questionnaires(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    List questionnaires

    - **Patients**: See only their own questionnaires
    - **Doctors**: See all questionnaires
    """
    query = db.query(Questionnaire)

    # Patients can only see their own questionnaires
    if current_user.role.value == "patient":
        query = query.filter(Questionnaire.patient_id == current_user.id)

    questionnaires = query.offset(skip).limit(limit).all()
    return questionnaires


@router.get("/{questionnaire_id}", response_model=QuestionnaireResponse)
def get_questionnaire(
    questionnaire_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific questionnaire by ID

    - **Patients**: Can only view their own questionnaires
    - **Doctors**: Can view any questionnaire
    """
    questionnaire = db.query(Questionnaire).filter(Questionnaire.id == questionnaire_id).first()

    if not questionnaire:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Questionnaire not found"
        )

    # Patients can only access their own questionnaires
    if current_user.role.value == "patient" and questionnaire.patient_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this questionnaire"
        )

    return questionnaire


@router.put("/{questionnaire_id}", response_model=QuestionnaireResponse)
def update_questionnaire(
    questionnaire_id: int,
    questionnaire_data: QuestionnaireUpdate,
    current_user: User = Depends(get_current_active_patient),
    db: Session = Depends(get_db)
):
    """
    Update a questionnaire (patients only, only their own drafts)

    Can only update questionnaires in DRAFT status
    """
    questionnaire = db.query(Questionnaire).filter(
        Questionnaire.id == questionnaire_id,
        Questionnaire.patient_id == current_user.id
    ).first()

    if not questionnaire:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Questionnaire not found"
        )

    if questionnaire.status != QuestionnaireStatus.DRAFT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only update questionnaires in DRAFT status"
        )

    # Update fields
    update_data = questionnaire_data.dict(exclude_unset=True)

    # Recalculate BMI if height/weight changed
    if any(k in update_data for k in ["height_ft", "height_in", "weight_lb"]):
        screener = ScreeningService()
        bmi = screener.calculate_bmi(
            update_data.get("height_ft", questionnaire.height_ft),
            update_data.get("height_in", questionnaire.height_in),
            update_data.get("weight_lb", questionnaire.weight_lb)
        )
        update_data["bmi"] = bmi

    for field, value in update_data.items():
        setattr(questionnaire, field, value)

    db.commit()
    db.refresh(questionnaire)

    return questionnaire


@router.post("/{questionnaire_id}/submit", response_model=QuestionnaireResponse)
def submit_questionnaire(
    questionnaire_id: int,
    db: Session = Depends(get_db)
):
    """
    Submit a questionnaire for screening (public access - no authentication required)

    Changes status from DRAFT to SUBMITTED and triggers screening
    """
    questionnaire = db.query(Questionnaire).filter(
        Questionnaire.id == questionnaire_id
    ).first()

    if not questionnaire:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Questionnaire not found"
        )

    if questionnaire.status != QuestionnaireStatus.DRAFT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Questionnaire already submitted"
        )

    # Update status
    questionnaire.status = QuestionnaireStatus.SUBMITTED
    questionnaire.submitted_at = datetime.utcnow()

    db.commit()
    db.refresh(questionnaire)

    return questionnaire


@router.delete("/{questionnaire_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_questionnaire(
    questionnaire_id: int,
    current_user: User = Depends(get_current_active_patient),
    db: Session = Depends(get_db)
):
    """
    Delete a questionnaire (patients only, only their own drafts)

    Can only delete questionnaires in DRAFT status
    """
    questionnaire = db.query(Questionnaire).filter(
        Questionnaire.id == questionnaire_id,
        Questionnaire.patient_id == current_user.id
    ).first()

    if not questionnaire:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Questionnaire not found"
        )

    if questionnaire.status != QuestionnaireStatus.DRAFT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only delete questionnaires in DRAFT status"
        )

    db.delete(questionnaire)
    db.commit()

    return None
