"""
Test script to demonstrate the screening algorithm
Run this to see how the screening works with sample patient data
"""

from app.services.screening_service import ScreeningService
import json


def test_eligible_patient():
    """Test case: Eligible patient with BMI 32, no major contraindications"""
    print("=" * 80)
    print("TEST CASE 1: Eligible Patient with Obesity")
    print("=" * 80)

    patient_data = {
        # Basic info
        "age": 35,
        "gender": "female",
        "is_childbearing_age_woman": True,

        # Eligibility
        "has_medical_evaluation": True,
        "attempted_lifestyle_modifications": True,
        "has_reliable_contraception": True,
        "bariatric_surgery_status": "not_applicable",

        # BMI (5'4", 185 lbs = BMI ~31.7)
        "height_ft": 5,
        "height_in": 4,
        "weight_lb": 185,

        # Comorbidities
        "comorbidities": ["hypertension", "type_2_diabetes"],

        # Symptoms
        "symptoms": ["excessive_appetite", "lack_satiety", "emotional_eating"],

        # Health conditions
        "health_conditions": ["controlled_hypertension", "type_2_diabetes"],
    }

    screener = ScreeningService()
    result = screener.run_screening(patient_data)

    print(f"\n📊 SCREENING RESULTS:")
    print(f"   Eligible: {result['is_eligible']}")
    print(f"   BMI: {result['bmi']}")
    print(f"   Category: {result['bmi_category']}")
    print(f"   Message: {result['eligibility_message']}")

    print(f"\n🔍 SCREENING STEPS:")
    for step in result['screening_steps']:
        print(f"   {step['step']}: {step['result']}")

    if result['excluded_drugs']:
        print(f"\n❌ EXCLUDED MEDICATIONS:")
        for drug, reason in result['excluded_drugs'].items():
            print(f"   - {drug}: {reason}")

    if result['recommended_drugs']:
        print(f"\n✅ RECOMMENDED MEDICATIONS (in priority order):")
        for rec in result['recommended_drugs']:
            print(f"   {rec['priority']}. {rec['medication']}")
            print(f"      → {rec['reasoning']}")

    if result['warnings']:
        print(f"\n⚠️  WARNINGS & CONSIDERATIONS:")
        for warning in result['warnings']:
            print(f"   {warning}")

    print("\n" + "=" * 80 + "\n")


def test_ineligible_low_bmi():
    """Test case: Ineligible patient - BMI too low without comorbidities"""
    print("=" * 80)
    print("TEST CASE 2: Ineligible Patient (Low BMI, No Comorbidities)")
    print("=" * 80)

    patient_data = {
        "has_medical_evaluation": True,
        "attempted_lifestyle_modifications": True,
        "has_reliable_contraception": True,
        "bariatric_surgery_status": "not_applicable",
        "is_childbearing_age_woman": False,

        # BMI 28 without comorbidities
        "height_ft": 5,
        "height_in": 6,
        "weight_lb": 170,

        "comorbidities": [],
        "symptoms": ["excessive_appetite"],
        "health_conditions": [],
    }

    screener = ScreeningService()
    result = screener.run_screening(patient_data)

    print(f"\n📊 SCREENING RESULTS:")
    print(f"   Eligible: {result['is_eligible']}")
    print(f"   BMI: {result['bmi']}")
    print(f"   Category: {result['bmi_category']}")
    print(f"   Message: {result['eligibility_message']}")

    print("\n" + "=" * 80 + "\n")


def test_patient_with_contraindications():
    """Test case: Patient with multiple contraindications"""
    print("=" * 80)
    print("TEST CASE 3: Patient with Contraindications")
    print("=" * 80)

    patient_data = {
        "has_medical_evaluation": True,
        "attempted_lifestyle_modifications": True,
        "has_reliable_contraception": False,
        "bariatric_surgery_status": "not_applicable",
        "is_childbearing_age_woman": False,

        # BMI 35 (Class 2 Obesity)
        "height_ft": 5,
        "height_in": 8,
        "weight_lb": 230,

        "comorbidities": ["hypertension", "type_2_diabetes"],
        "symptoms": ["binge_eating", "night_eating"],
        "health_conditions": [
            "uncontrolled_hypertension",
            "glaucoma_unstable",
            "substance_abuse_history"
        ],
    }

    screener = ScreeningService()
    result = screener.run_screening(patient_data)

    print(f"\n📊 SCREENING RESULTS:")
    print(f"   Eligible: {result['is_eligible']}")
    print(f"   BMI: {result['bmi']}")
    print(f"   Category: {result['bmi_category']}")

    print(f"\n🔍 SCREENING STEPS:")
    for step in result['screening_steps']:
        print(f"   {step['step']}: {step['result']}")

    if result['excluded_drugs']:
        print(f"\n❌ EXCLUDED MEDICATIONS ({len(result['excluded_drugs'])} total):")
        for drug, reason in result['excluded_drugs'].items():
            print(f"   - {drug}: {reason}")

    if result['recommended_drugs']:
        print(f"\n✅ RECOMMENDED MEDICATIONS (in priority order):")
        for rec in result['recommended_drugs']:
            print(f"   {rec['priority']}. {rec['medication']}")
            print(f"      → {rec['reasoning']}")
    else:
        print(f"\n⚠️  No medications can be safely recommended.")
        print(f"   Consider Orlistat as last resort option.")

    if result['warnings']:
        print(f"\n⚠️  WARNINGS & CONSIDERATIONS:")
        for warning in result['warnings']:
            print(f"   {warning}")

    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    print("\n🏥 AOM SCREENING ALGORITHM - TEST SUITE\n")

    # Run all test cases
    test_eligible_patient()
    test_ineligible_low_bmi()
    test_patient_with_contraindications()

    print("✅ All tests completed!")
