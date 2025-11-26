"""
AOM Screening Service
Implements the 2-step screening mechanism from the new questionnaire
Updated to distinguish ABSOLUTE vs RELATIVE contraindications
"""

from typing import Dict, List, Tuple, Any
from enum import Enum


class ContraindicationType(str, Enum):
    """Types of contraindications"""
    ABSOLUTE = "absolute"  # Hard eliminate
    RELATIVE = "relative"  # Caution/requires clearance

class DrugName(str, Enum):
    """Available medications"""
    PHENTERMINE = "Phentermine"
    TOPIRAMATE = "Topiramate"
    QSYMIA = "Qsymia"
    CONTRAVE = "Contrave"
    NALTREXONE = "Naltrexone"
    BUPROPION = "Bupropion"
    VYVANSE = "Vyvanse"
    WEGOVY = "Wegovy"
    ZEPBOUND = "Zepbound"


# Initial drug pool - order matters for Second-Step display
INITIAL_DRUG_POOL = [
    DrugName.PHENTERMINE,
    DrugName.TOPIRAMATE,
    DrugName.QSYMIA,
    DrugName.CONTRAVE,
    DrugName.NALTREXONE,
    DrugName.BUPROPION,
    DrugName.VYVANSE,
    DrugName.WEGOVY,
    DrugName.ZEPBOUND,
]


class ScreeningService:
    """Service to handle medication screening logic"""

    @staticmethod
    def calculate_bmi(height_ft: int, height_in: int, weight_lb: float) -> float:
        """Calculate BMI from imperial units"""
        total_inches = (height_ft * 12) + height_in
        height_m = total_inches * 0.0254
        weight_kg = weight_lb * 0.453592
        bmi = weight_kg / (height_m ** 2)
        return round(bmi, 2)

    @staticmethod
    def apply_first_step_exclusions(
        health_conditions: List[str],
        condition_control_status: Dict[str, str] = None
    ) -> Tuple[List[str], Dict[str, str], Dict[str, str]]:
        """
        First-Step: Health Status Exclusions Based on Table 1 from AMO Questionnaire Document
        Returns: (remaining_drugs, absolute_exclusions, relative_warnings)

        - Absolute exclusions: Hard eliminate from drug pool
        - Relative warnings: Keep in pool but flag for caution/clearance

        Table 1 has exactly 11 rows:
        Row 1-9: ABSOLUTE contraindications (hard remove)
        Row 10-11: RELATIVE contraindications (flag for caution)
        """
        remaining_drugs = INITIAL_DRUG_POOL.copy()
        absolute_exclusions = {}  # Hard eliminate
        relative_warnings = {}     # Caution/requires clearance

        # Default to empty dict if not provided
        if condition_control_status is None:
            condition_control_status = {}

        # 🚨 PREGNANCY CHECK: Per document - "Checking pregnancy disqualifies the patient from AOM criteria"
        if "pregnancy_breastfeeding" in health_conditions:
            for drug in INITIAL_DRUG_POOL:
                absolute_exclusions[drug] = "⛔ ABSOLUTE: Current pregnancy disqualifies ALL anti-obesity medications. Reassess postpartum."
            return [], absolute_exclusions, relative_warnings

        for condition in health_conditions:
            # ===== TABLE 1 - ABSOLUTE CONTRAINDICATIONS (Rows 1-9) =====

            # Row 1 & Row 10: Hypertension (depends on controlled/uncontrolled status)
            # - Uncontrolled → ABSOLUTE: Remove 5 drugs
            # - Controlled → RELATIVE: Flag for caution (NOT REMOVED)
            if condition == "hypertension":
                control_status = condition_control_status.get("hypertension", "uncontrolled")

                if control_status == "controlled":
                    # Row 10: Controlled hypertension → FLAG for caution (NOT REMOVED)
                    drugs_to_flag = [DrugName.PHENTERMINE, DrugName.VYVANSE, DrugName.QSYMIA, DrugName.CONTRAVE, DrugName.BUPROPION]
                    for drug in drugs_to_flag:
                        if drug not in relative_warnings:
                            relative_warnings[drug] = "⚠️ RELATIVE: Hypertension (controlled) - Use with BP re-evaluation. Adjust dosage if needed."
                else:
                    # Row 1: Uncontrolled hypertension → ABSOLUTE removal
                    drugs_to_remove = [DrugName.PHENTERMINE, DrugName.VYVANSE, DrugName.QSYMIA, DrugName.CONTRAVE, DrugName.BUPROPION]
                    for drug in drugs_to_remove:
                        if drug in remaining_drugs:
                            remaining_drugs.remove(drug)
                            absolute_exclusions[drug] = "⛔ ABSOLUTE: Hypertension (uncontrolled) - Contraindicated. Hard eliminate."

            # Row 2: Recurrent kidney stones/Planning pregnancy/Currently pregnant → Remove Qsymia, Topiramate
            elif condition == "recurrent_kidney_stones":
                drugs_to_remove = [DrugName.QSYMIA, DrugName.TOPIRAMATE]
                for drug in drugs_to_remove:
                    if drug in remaining_drugs:
                        remaining_drugs.remove(drug)
                        absolute_exclusions[drug] = "⛔ ABSOLUTE: Recurrent kidney stones - Topiramate increases stone risk. Hard eliminate."

            elif condition == "planning_pregnancy":
                drugs_to_remove = [DrugName.QSYMIA, DrugName.TOPIRAMATE]
                for drug in drugs_to_remove:
                    if drug in remaining_drugs:
                        remaining_drugs.remove(drug)
                        absolute_exclusions[drug] = "⛔ ABSOLUTE: Planning pregnancy within 3 months - Teratogenic risk. Hard eliminate."

            # Row 3: Taking Tamoxifen → Remove Contrave, Bupropion
            elif condition == "taking_tamoxifen":
                drugs_to_remove = [DrugName.CONTRAVE, DrugName.BUPROPION]
                for drug in drugs_to_remove:
                    if drug in remaining_drugs:
                        remaining_drugs.remove(drug)
                        absolute_exclusions[drug] = "⛔ ABSOLUTE: Taking Tamoxifen - Drug interaction. Hard eliminate."

            # Row 4: ADD/ADHD (under medication) → Remove Phentermine, Vyvanse, Qsymia
            elif condition == "adhd":
                drugs_to_remove = [DrugName.PHENTERMINE, DrugName.VYVANSE, DrugName.QSYMIA]
                for drug in drugs_to_remove:
                    if drug in remaining_drugs:
                        remaining_drugs.remove(drug)
                        absolute_exclusions[drug] = "⛔ ABSOLUTE: ADD/ADHD under medication treatment - Contraindicated. Hard eliminate."

            # Row 5: Glaucoma (not stable) → Remove Phentermine, Qsymia, Topiramate, Vyvanse
            elif condition == "glaucoma":
                drugs_to_remove = [DrugName.PHENTERMINE, DrugName.QSYMIA, DrugName.TOPIRAMATE, DrugName.VYVANSE]
                for drug in drugs_to_remove:
                    if drug in remaining_drugs:
                        remaining_drugs.remove(drug)
                        absolute_exclusions[drug] = "⛔ ABSOLUTE: Glaucoma (not evaluated as stable) - Contraindicated. Hard eliminate."

            # Row 6: History of stroke/Intracranial hypertension/Cardiovascular disease → Remove Phentermine, Vyvanse, Qsymia
            elif condition in ["cva_stroke", "intracranial_hypertension", "cad", "mi",
                              "cerebrovascular_disease", "pad"]:
                drugs_to_remove = [DrugName.PHENTERMINE, DrugName.VYVANSE, DrugName.QSYMIA]
                condition_display = condition.replace('_', ' ').title()
                for drug in drugs_to_remove:
                    if drug in remaining_drugs:
                        remaining_drugs.remove(drug)
                        absolute_exclusions[drug] = f"⛔ ABSOLUTE: {condition_display} - Cardiovascular contraindication. Hard eliminate."

            # Row 7: History of substance abuse → Remove Phentermine, Vyvanse, Qsymia
            elif condition == "substance_abuse":
                drugs_to_remove = [DrugName.PHENTERMINE, DrugName.VYVANSE, DrugName.QSYMIA]
                for drug in drugs_to_remove:
                    if drug in remaining_drugs:
                        remaining_drugs.remove(drug)
                        absolute_exclusions[drug] = "⛔ ABSOLUTE: Substance abuse history - Controlled substance risk. Hard eliminate."

            # Row 8: Hyperthyroidism → Remove Phentermine, Qsymia
            elif condition == "hyperthyroidism":
                drugs_to_remove = [DrugName.PHENTERMINE, DrugName.QSYMIA]
                for drug in drugs_to_remove:
                    if drug in remaining_drugs:
                        remaining_drugs.remove(drug)
                        absolute_exclusions[drug] = "⛔ ABSOLUTE: Hyperthyroidism - Contraindicated. Hard eliminate."

            # Row 9: Medullary thyroid cancer/Pancreatitis/Gastroparesis → Remove Wegovy, Zepbound
            elif condition in ["medullary_thyroid_cancer", "pancreatitis", "gastroparesis"]:
                drugs_to_remove = [DrugName.WEGOVY, DrugName.ZEPBOUND]
                condition_display = condition.replace('_', ' ').title()
                for drug in drugs_to_remove:
                    if drug in remaining_drugs:
                        remaining_drugs.remove(drug)
                        absolute_exclusions[drug] = f"⛔ ABSOLUTE: {condition_display} - GLP-1 contraindicated. Hard eliminate."

            # ===== TABLE 1 - RELATIVE CONTRAINDICATIONS (Rows 10-11) =====
            # These are FLAGS, not removals - drugs stay in pool with warnings

            # Row 10: Hypertension (controlled) → Flag for caution (NOT REMOVED)
            # Note: This is handled separately - will need controlled/uncontrolled status from frontend
            # For now, leaving as placeholder for future implementation

            # Row 11: Psychiatric disorders (bipolar disorder, stable) → Flag for psychiatrist clearance
            elif condition == "psychiatric_treatment":
                drugs_to_flag = [DrugName.PHENTERMINE, DrugName.VYVANSE, DrugName.QSYMIA, DrugName.CONTRAVE]
                for drug in drugs_to_flag:
                    if drug not in relative_warnings:
                        relative_warnings[drug] = "⚠️ RELATIVE: Psychiatric disorders (bipolar, stable) - Must confirm with psychiatrist. Attach written approval before prescription."

        return remaining_drugs, absolute_exclusions, relative_warnings

    @staticmethod
    def apply_second_step_ordering(
        drug_pool: List[str],
        eating_habits: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Second-Step: Display Order Adjustment Based on Eating Habits & Feelings
        Returns prioritized list of medications
        """
        # Categorize eating habits
        appetite_issues = {"excessive_appetite", "lack_of_satiety", "binge_eating"}
        behavioral_issues = {"emotional_eating", "night_eating", "frequent_snacking"}

        checked_appetite = appetite_issues.intersection(set(eating_habits))
        checked_behavioral = behavioral_issues.intersection(set(eating_habits))

        has_appetite = len(checked_appetite) > 0
        has_behavioral = len(checked_behavioral) > 0

        # Determine priority order
        if has_appetite and has_behavioral:
            # Scenario 3: Both types checked
            priority_order = [DrugName.QSYMIA, DrugName.CONTRAVE]
        elif has_appetite:
            # Scenario 1: Items 1-3 checked (appetite issues)
            priority_order = [DrugName.PHENTERMINE, DrugName.VYVANSE, DrugName.QSYMIA, DrugName.TOPIRAMATE]
        elif has_behavioral:
            # Scenario 2: Items 4-6 checked (behavioral/emotional)
            priority_order = [DrugName.CONTRAVE, DrugName.TOPIRAMATE, DrugName.NALTREXONE, DrugName.BUPROPION]
        else:
            # Scenario 4: None checked - maintain original order
            priority_order = []

        # Build final recommendations list
        recommendations = []

        # Add prioritized drugs first
        for drug in priority_order:
            if drug in drug_pool:
                recommendations.append({
                    "medication": drug,
                    "priority": len(recommendations) + 1,
                    "reasoning": "Retained after screening"
                })

        # Add remaining drugs in original order
        for drug in INITIAL_DRUG_POOL:
            if drug in drug_pool and drug not in priority_order:
                recommendations.append({
                    "medication": drug,
                    "priority": len(recommendations) + 1,
                    "reasoning": "Retained after screening"
                })

        return recommendations

    def run_screening(self, questionnaire_data: Dict) -> Dict[str, Any]:
        """
        Main screening function - runs the 2-step mechanism per AMO Questionnaire Document

        Eligibility Gate: Only "no comorbidities + BMI <30" = ineligible
        - BMI ≥30: Eligible (even without comorbidities)
        - BMI 27-29.9 + comorbidities: Eligible

        Returns complete screening results with ABSOLUTE and RELATIVE contraindications
        """
        result = {
            "is_eligible": True,
            "eligibility_message": "Screening completed",
            "bmi": None,
            "bmi_category": None,
            "initial_drug_pool": INITIAL_DRUG_POOL.copy(),
            "absolute_exclusions": {},      # Hard eliminated
            "relative_warnings": {},        # Requires caution/clearance
            "recommended_drugs": [],
            "warnings": [],
            "screening_steps": []
        }

        # Calculate BMI
        bmi = self.calculate_bmi(
            questionnaire_data["height_ft"],
            questionnaire_data["height_in"],
            questionnaire_data["weight_lb"]
        )
        result["bmi"] = bmi
        result["bmi_category"] = str(bmi)

        # ⛔ ELIGIBILITY GATE: Per AMO Questionnaire Document
        # "Only people with 'no comorbidities + BMI <30' are not eligible for oral AOM"
        # "those with BMI ≥30 may can go to next step even with no comorbidities"
        health_conditions = questionnaire_data.get("health_conditions", [])

        # Check if patient has any comorbidities (excluding "none")
        has_comorbidities = len([c for c in health_conditions if c != "none"]) > 0

        # Only ineligible if BOTH conditions are true: no comorbidities AND BMI < 30
        if not has_comorbidities and bmi < 30:
            result["is_eligible"] = False
            result["eligibility_message"] = "Not eligible for oral anti-obesity medications"
            result["warnings"] = [
                "⛔ BMI Requirement Not Met: Your BMI is below 30 with no comorbidities.",
                "Oral anti-obesity medications are indicated for individuals with:",
                "• BMI ≥ 30, OR",
                "• BMI ≥ 27 with weight-related comorbidities (e.g., hypertension, diabetes, sleep apnea)",
                "",
                "Your BMI: {:.2f}".format(bmi),
                "",
                "💡 Recommendation: Focus on lifestyle modifications including diet and exercise.",
                "Please consult with your healthcare provider for personalized weight management strategies."
            ]
            result["screening_steps"].append({
                "step": "BMI Eligibility Gate",
                "result": f"BMI {bmi:.2f} < 30 with no comorbidities: Not eligible. No further screening performed."
            })
            # Return early - skip all comorbidity and drug screening
            return result

        # Eligible: Either BMI ≥30 OR BMI 27-29.9 with comorbidities
        eligibility_reason = "BMI ≥ 30" if bmi >= 30 else f"BMI {bmi:.2f} ≥ 27 with comorbidities"
        result["screening_steps"].append({
            "step": "BMI Eligibility Gate",
            "result": f"{eligibility_reason}: Passed eligibility gate. Proceeding to comorbidity assessment."
        })

        # FIRST-STEP: Apply health status exclusions (Table 1)
        condition_control_status = questionnaire_data.get("condition_control_status", {})
        remaining_drugs, absolute_exclusions, relative_warnings = self.apply_first_step_exclusions(
            health_conditions,
            condition_control_status
        )

        result["absolute_exclusions"] = absolute_exclusions
        result["relative_warnings"] = relative_warnings

        # Create comprehensive warnings list
        if absolute_exclusions:
            result["warnings"].append(f"⛔ {len(absolute_exclusions)} medications have ABSOLUTE contraindications and are hard eliminated.")
        if relative_warnings:
            result["warnings"].append(f"⚠️ {len(relative_warnings)} medications have RELATIVE contraindications. Caution/clearance required.")

        result["screening_steps"].append({
            "step": "First-Step - Health Status Exclusions (Table 1)",
            "result": f"ABSOLUTE exclusions: {len(absolute_exclusions)}. RELATIVE warnings: {len(relative_warnings)}. Remaining eligible: {len(remaining_drugs)}"
        })

        # SECOND-STEP: Apply eating habits-based ordering
        eating_habits = questionnaire_data.get("eating_habits", [])
        recommendations = self.apply_second_step_ordering(remaining_drugs, eating_habits)

        result["recommended_drugs"] = recommendations
        result["screening_steps"].append({
            "step": "Second-Step - Eating Habits Display Order",
            "result": f"Generated {len(recommendations)} ordered recommendations based on eating habits"
        })

        return result
