"""
AOM Screening Service
Implements the 2-step screening mechanism from the new questionnaire
"""

from typing import Dict, List, Tuple, Any
from enum import Enum


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
        health_conditions: List[str]
    ) -> Tuple[List[str], Dict[str, str]]:
        """
        First-Step: Health Status Exclusions Based on Table 1
        Returns: (remaining_drugs, excluded_drugs_with_reasons)
        """
        remaining_drugs = INITIAL_DRUG_POOL.copy()
        excluded = {}

        for condition in health_conditions:
            # Row 1: Hypertension
            if condition == "hypertension":
                drugs_to_remove = [DrugName.PHENTERMINE, DrugName.VYVANSE, DrugName.QSYMIA, DrugName.CONTRAVE, DrugName.BUPROPION]
                for drug in drugs_to_remove:
                    if drug in remaining_drugs:
                        remaining_drugs.remove(drug)
                        excluded[drug] = "Excluded: Hypertension"

            # Row 2: Recurrent kidney stones OR Planning pregnancy (within 3 months) OR Currently pregnant
            elif condition in ["recurrent_kidney_stones", "planning_pregnancy", "pregnancy_breastfeeding"]:
                drugs_to_remove = [DrugName.QSYMIA, DrugName.TOPIRAMATE]
                for drug in drugs_to_remove:
                    if drug in remaining_drugs:
                        remaining_drugs.remove(drug)
                        excluded[drug] = f"Excluded: {condition.replace('_', ' ').title()}"

            # Row 3: Taking Tamoxifen
            elif condition == "taking_tamoxifen":
                drugs_to_remove = [DrugName.CONTRAVE, DrugName.BUPROPION]
                for drug in drugs_to_remove:
                    if drug in remaining_drugs:
                        remaining_drugs.remove(drug)
                        excluded[drug] = "Excluded: Currently taking Tamoxifen"

            # Row 4: ADD/ADHD
            elif condition == "adhd":
                drugs_to_remove = [DrugName.PHENTERMINE, DrugName.VYVANSE, DrugName.QSYMIA]
                for drug in drugs_to_remove:
                    if drug in remaining_drugs:
                        remaining_drugs.remove(drug)
                        excluded[drug] = "Excluded: ADD/ADHD"

            # Row 5: Glaucoma
            elif condition == "glaucoma":
                drugs_to_remove = [DrugName.PHENTERMINE, DrugName.QSYMIA, DrugName.TOPIRAMATE, DrugName.VYVANSE]
                for drug in drugs_to_remove:
                    if drug in remaining_drugs:
                        remaining_drugs.remove(drug)
                        excluded[drug] = "Excluded: Glaucoma"

            # Row 6: Stroke OR Intracranial hypertension OR Cardiovascular disease
            elif condition in ["history_stroke", "intracranial_hypertension", "heart_disease"]:
                drugs_to_remove = [DrugName.PHENTERMINE, DrugName.VYVANSE, DrugName.QSYMIA]
                for drug in drugs_to_remove:
                    if drug in remaining_drugs:
                        remaining_drugs.remove(drug)
                        excluded[drug] = f"Excluded: {condition.replace('_', ' ').title()}"

            # Row 7: Psychiatric disorders
            elif condition == "psychiatric_treatment":
                drugs_to_remove = [DrugName.CONTRAVE, DrugName.BUPROPION, DrugName.TOPIRAMATE, DrugName.QSYMIA]
                for drug in drugs_to_remove:
                    if drug in remaining_drugs:
                        remaining_drugs.remove(drug)
                        excluded[drug] = "Excluded: Psychiatric disorders"

            # Row 8: History of substance abuse
            elif condition == "history_drug_abuse":
                drugs_to_remove = [DrugName.PHENTERMINE, DrugName.VYVANSE, DrugName.QSYMIA]
                for drug in drugs_to_remove:
                    if drug in remaining_drugs:
                        remaining_drugs.remove(drug)
                        excluded[drug] = "Excluded: History of substance abuse"

            # Row 9: Thyroid dysfunction (hyperthyroidism/hypothyroidism)
            elif condition == "hyperthyroidism":
                drugs_to_remove = [DrugName.PHENTERMINE, DrugName.QSYMIA]
                for drug in drugs_to_remove:
                    if drug in remaining_drugs:
                        remaining_drugs.remove(drug)
                        excluded[drug] = "Excluded: Thyroid dysfunction"

            # Row 10: Medullary thyroid cancer OR Pancreatitis OR Gastroparesis
            elif condition in ["thyroid_cancer", "history_pancreatitis", "gastroparesis"]:
                drugs_to_remove = [DrugName.WEGOVY, DrugName.ZEPBOUND]
                for drug in drugs_to_remove:
                    if drug in remaining_drugs:
                        remaining_drugs.remove(drug)
                        excluded[drug] = f"Excluded: {condition.replace('_', ' ').title()}"

        return remaining_drugs, excluded

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
        Main screening function - runs the 2-step mechanism
        Returns complete screening results
        """
        result = {
            "is_eligible": True,
            "eligibility_message": "Screening completed",
            "bmi": None,
            "bmi_category": None,
            "initial_drug_pool": INITIAL_DRUG_POOL.copy(),
            "excluded_drugs": {},
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

        # Determine BMI category
        if bmi < 27:
            bmi_category = f"BMI {bmi} (Below threshold)"
        elif 27 <= bmi < 30:
            bmi_category = f"BMI {bmi} (Overweight)"
        elif 30 <= bmi < 35:
            bmi_category = f"BMI {bmi} (Class 1 Obesity)"
        elif 35 <= bmi < 40:
            bmi_category = f"BMI {bmi} (Class 2 Obesity)"
        else:
            bmi_category = f"BMI {bmi} (Class 3 Obesity)"

        result["bmi_category"] = bmi_category

        # FIRST-STEP: Apply health status exclusions (Table 1)
        health_conditions = questionnaire_data.get("health_conditions", [])
        remaining_drugs, excluded = self.apply_first_step_exclusions(health_conditions)

        result["excluded_drugs"] = excluded
        result["screening_steps"].append({
            "step": "First-Step - Health Status Exclusions",
            "result": f"Excluded {len(excluded)} medications based on health conditions. Remaining: {len(remaining_drugs)}"
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
