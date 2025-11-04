"""
AOM Screening Service
Implements the 4-step screening mechanism from the questionnaire
"""

from typing import Dict, List, Tuple, Any
from enum import Enum


class DrugName(str, Enum):
    """Available medications"""
    PHENTERMINE = "Phentermine"
    QSYMIA = "Qsymia (Phentermine/Topiramate)"
    CONTRAVE = "Contrave (Naltrexone/Bupropion)"
    SAXENDA = "Saxenda (Liraglutide)"
    WEGOVY = "Wegovy (Semaglutide)"
    ZEPBOUND = "Zepbound (Tirzepatide)"
    TOPIRAMATE = "Topiramate"
    NALTREXONE = "Naltrexone"
    BUPROPION = "Bupropion"
    VYVANSE = "Vyvanse"
    ORLISTAT = "Orlistat (Xenical/Alli)"


# Initial drug pool
INITIAL_DRUG_POOL = [
    DrugName.PHENTERMINE,
    DrugName.QSYMIA,
    DrugName.CONTRAVE,
    DrugName.SAXENDA,
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
    def check_eligibility(questionnaire_data: Dict) -> Tuple[bool, str]:
        """
        Step I: Confirm Patient Eligibility for Oral AOMs
        All conditions must be met, otherwise return False
        """
        # Condition 1: Medical evaluation completed
        if not questionnaire_data.get("has_medical_evaluation"):
            return False, "No medical evaluation completed. Temporarily ineligible for oral AOMs."

        # Condition 2: Lifestyle modifications attempted
        if not questionnaire_data.get("attempted_lifestyle_modifications"):
            return False, "Lifestyle modifications not attempted for ≥1 month. Temporarily ineligible for oral AOMs."

        # NOTE: Contraception requirement is now handled in contraindication step
        # to allow other medications besides Topiramate/Qsymia

        # Condition 4: Bariatric surgery check
        bariatric_status = questionnaire_data.get("bariatric_surgery_status")
        if bariatric_status == "yes":
            # Must be ≥6 months post-surgery with slow progress
            # This would need additional fields in the questionnaire
            # For now, we'll assume if they answered "yes", they meet criteria
            pass

        return True, "Patient meets all eligibility criteria for oral AOMs."

    @staticmethod
    def determine_bmi_eligibility(bmi: float, comorbidities: List[str]) -> Tuple[bool, str, List[str]]:
        """
        Step II: Determination of Eligibility Based on BMI + Comorbidities
        Returns: (is_eligible, bmi_category, initial_drug_pool)
        """
        # BMI < 27: Not eligible
        if bmi < 27:
            return False, "BMI 25-27.9 (Overweight)", []

        # BMI 27-29.9: Eligible only with comorbidities
        if 27 <= bmi < 30:
            if not comorbidities or len(comorbidities) == 0:
                return False, "BMI 27-29.9 without comorbidities", []
            return True, "BMI 27-29.9 with comorbidities", INITIAL_DRUG_POOL.copy()

        # BMI 30+: Eligible regardless of comorbidities
        if 30 <= bmi < 35:
            category = "BMI 30-34.9 (Class 1 Obesity)"
        elif 35 <= bmi < 40:
            category = "BMI 35-39.9 (Class 2 Obesity)"
        else:
            category = "BMI 40+ (Class 3 Obesity)"

        return True, category, INITIAL_DRUG_POOL.copy()

    @staticmethod
    def exclude_contraindicated_drugs(
        drug_pool: List[str],
        health_conditions: List[str],
        questionnaire_data: Dict = None
    ) -> Tuple[List[str], Dict[str, str], List[str]]:
        """
        Step III: Exclude Contraindicated Drugs Based on Health Conditions
        Returns: (remaining_drugs, excluded_drugs_with_reasons, special_notes)
        """
        remaining_drugs = drug_pool.copy()
        excluded = {}
        special_notes = []

        # Check for woman without reliable contraception
        if questionnaire_data:
            if questionnaire_data.get("is_childbearing_age_woman") and not questionnaire_data.get("has_reliable_contraception"):
                drugs_to_remove = [DrugName.TOPIRAMATE, DrugName.QSYMIA]
                for drug in drugs_to_remove:
                    if drug in remaining_drugs:
                        remaining_drugs.remove(drug)
                        excluded[drug] = "Contraindicated: Woman of childbearing age without reliable contraception"

        for condition in health_conditions:
            # Uncontrolled hypertension
            # Rule: Avoid Phentermine, Vyvanse, Qsymia, Contrave, Bupropion until BP controlled
            # Use: Topiramate and Naltrexone
            if condition == "uncontrolled_hypertension":
                drugs_to_remove = [DrugName.PHENTERMINE, DrugName.VYVANSE, DrugName.QSYMIA, DrugName.CONTRAVE, DrugName.BUPROPION]
                for drug in drugs_to_remove:
                    if drug in remaining_drugs:
                        remaining_drugs.remove(drug)
                        excluded[drug] = "Contraindicated: Uncontrolled hypertension. Consider after BP control."
                special_notes.append("Recommended: Topiramate and Naltrexone for uncontrolled hypertension")

            # Recurrent kidney stones / Planning pregnancy
            # Rule: Avoid Topiramate, Qsymia; Use Phentermine for short and intermittent use
            elif condition in ["recurrent_kidney_stones", "planning_pregnancy", "pregnancy_breastfeeding"]:
                drugs_to_remove = [DrugName.TOPIRAMATE, DrugName.QSYMIA]
                for drug in drugs_to_remove:
                    if drug in remaining_drugs:
                        remaining_drugs.remove(drug)
                        excluded[drug] = f"Contraindicated: {condition.replace('_', ' ').title()}"
                if DrugName.PHENTERMINE in remaining_drugs:
                    special_notes.append("Phentermine: Use for short and intermittent use only for kidney stones/pregnancy planning")

            # Tamoxifen
            # Rule: Hard contraindication to Contrave, Bupropion
            elif condition == "taking_tamoxifen":
                drugs_to_remove = [DrugName.CONTRAVE, DrugName.BUPROPION]
                for drug in drugs_to_remove:
                    if drug in remaining_drugs:
                        remaining_drugs.remove(drug)
                        excluded[drug] = "Hard contraindication: Taking Tamoxifen"

            # ADD/ADHD under medication treatment
            # Rule: Avoid Phentermine, Vyvanse
            elif condition == "adhd_on_medication":
                drugs_to_remove = [DrugName.PHENTERMINE, DrugName.VYVANSE]
                for drug in drugs_to_remove:
                    if drug in remaining_drugs:
                        remaining_drugs.remove(drug)
                        excluded[drug] = "Contraindicated: ADD/ADHD under medication treatment"

            # Glaucoma
            # Rule: Avoid Phentermine, Qsymia, Topiramate, Vyvanse (unless stable and cleared by optho)
            # Use: Contrave, Bupropion, Naltrexone
            elif condition == "glaucoma":
                drugs_to_remove = [DrugName.PHENTERMINE, DrugName.QSYMIA, DrugName.TOPIRAMATE, DrugName.VYVANSE]
                for drug in drugs_to_remove:
                    if drug in remaining_drugs:
                        remaining_drugs.remove(drug)
                        excluded[drug] = "Contraindicated: Glaucoma (unless stable and cleared by ophthalmologist)"
                special_notes.append("Recommended: Contrave, Bupropion, Naltrexone for glaucoma patients")

            # Intracranial HTN, Stroke, CVD
            # Rule: Avoid Phentermine, Vyvanse, Qsymia (unless stable and cleared by cards/neuro)
            # Use: Topiramate and Naltrexone
            elif condition in ["heart_disease", "history_stroke", "intracranial_hypertension"]:
                drugs_to_remove = [DrugName.PHENTERMINE, DrugName.VYVANSE, DrugName.QSYMIA]
                for drug in drugs_to_remove:
                    if drug in remaining_drugs:
                        remaining_drugs.remove(drug)
                        excluded[drug] = f"Contraindicated: {condition.replace('_', ' ').title()} (unless stable and cleared by cardiologist/neurologist)"
                special_notes.append("Recommended: Topiramate and Naltrexone for cardiovascular/neurological conditions")

            # Psychiatric Treatment
            # Rule: Prozac, Zoloft, anxiolytics generally okay
            # Avoid: Contrave, Bupropion, Topiramate (okay in special circumstances)
            # Use: Naltrexone, consider Phentermine (avoid in anxiety/bipolar)
            elif condition == "psychiatric_treatment":
                drugs_to_remove = [DrugName.CONTRAVE, DrugName.BUPROPION, DrugName.TOPIRAMATE]
                for drug in drugs_to_remove:
                    if drug in remaining_drugs:
                        remaining_drugs.remove(drug)
                        excluded[drug] = "Contraindicated: Psychiatric treatment (okay in special circumstances with provider approval)"
                special_notes.append("Recommended: Naltrexone for psychiatric patients. Phentermine may be considered (avoid if anxiety/bipolar).")
                special_notes.append("Note: Prozac, Zoloft, anxiolytics generally okay with AOMs")

            # History of drug abuse
            elif condition == "history_drug_abuse":
                drugs_to_remove = [DrugName.PHENTERMINE, DrugName.VYVANSE, DrugName.QSYMIA]
                for drug in drugs_to_remove:
                    if drug in remaining_drugs:
                        remaining_drugs.remove(drug)
                        excluded[drug] = "Contraindicated: History of substance abuse"

            # Hyperthyroidism
            elif condition == "hyperthyroidism":
                drugs_to_remove = [DrugName.PHENTERMINE, DrugName.QSYMIA]
                for drug in drugs_to_remove:
                    if drug in remaining_drugs:
                        remaining_drugs.remove(drug)
                        excluded[drug] = "Contraindicated: Uncontrolled hyperthyroidism"

            # History of pancreatitis
            elif condition == "history_pancreatitis":
                drugs_to_remove = [DrugName.SAXENDA, DrugName.WEGOVY, DrugName.ZEPBOUND]
                for drug in drugs_to_remove:
                    if drug in remaining_drugs:
                        remaining_drugs.remove(drug)
                        excluded[drug] = "Contraindicated: History of pancreatitis"

            # Thyroid cancer
            elif condition == "thyroid_cancer":
                drugs_to_remove = [DrugName.SAXENDA, DrugName.WEGOVY, DrugName.ZEPBOUND]
                for drug in drugs_to_remove:
                    if drug in remaining_drugs:
                        remaining_drugs.remove(drug)
                        excluded[drug] = "Contraindicated: Thyroid cancer or family history of MTC"

            # Gallbladder disease
            elif condition == "gallbladder_disease":
                special_notes.append("Caution: Monitor for gallbladder issues with GLP-1 agonists (Saxenda, Wegovy, Zepbound)")

            # Kidney disease
            elif condition == "kidney_disease":
                special_notes.append("Caution: Dose adjustment may be needed for kidney disease")

        return remaining_drugs, excluded, special_notes

    @staticmethod
    def prioritize_by_symptoms(
        drug_pool: List[str],
        symptoms: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Step IV: Refine Recommendation Priority Based on Symptoms
        Based on:
        - Large appetite/Lack of satiety/Binge eating: Phentermine, Vyvanse, Qsymia, Topiramate
        - Emotional Eating/Cravings/Night Eating/Snacking/Grazing: Contrave, Bupropion, Naltrexone, Topiramate
        """
        recommendations = []

        # Categorize symptoms per your rules
        appetite_symptoms = ["excessive_appetite", "binge_eating", "loss_of_control_eating"]
        behavioral_symptoms = ["emotional_eating"]

        has_appetite_issues = any(s in symptoms for s in appetite_symptoms)
        has_behavioral_issues = any(s in symptoms for s in behavioral_symptoms)
        has_binge_eating = "binge_eating" in symptoms

        if has_appetite_issues and has_behavioral_issues:
            # Mixed symptoms: prioritize drugs that address both
            priority_order = [
                (DrugName.QSYMIA, "First-line: Balances appetite suppression + eating behavior control"),
                (DrugName.TOPIRAMATE, "Alternative: Addresses both appetite and behavioral symptoms"),
                (DrugName.CONTRAVE, "Alternative: Good for mixed symptoms"),
                (DrugName.PHENTERMINE, "Alternative: Strong appetite suppressant"),
            ]
        elif has_appetite_issues:
            # Large appetite/Lack of satiety/Binge eating
            # Rule: Phentermine, Vyvanse, Qsymia, Topiramate
            priority_order = []
            if has_binge_eating:
                # Vyvanse is FDA-approved for binge eating disorder
                priority_order.append((DrugName.VYVANSE, "First-line: FDA-approved for binge eating disorder"))
            priority_order.extend([
                (DrugName.PHENTERMINE, "First-line: Cost-effective appetite suppressant"),
                (DrugName.QSYMIA, "Enhanced appetite control with longer duration"),
                (DrugName.TOPIRAMATE, "Alternative: Appetite suppression"),
            ])
            if not has_binge_eating and DrugName.VYVANSE in drug_pool:
                priority_order.insert(1, (DrugName.VYVANSE, "Alternative: Strong appetite control"))
        elif has_behavioral_issues:
            # Emotional Eating/Cravings/Night Eating/Snacking/Grazing
            # Rule: Contrave, Bupropion, Naltrexone, Topiramate
            priority_order = [
                (DrugName.CONTRAVE, "First-line: Targets cravings and emotional eating"),
                (DrugName.BUPROPION, "Alternative: Helps with emotional eating"),
                (DrugName.NALTREXONE, "Alternative: Reduces cravings and reward-based eating"),
                (DrugName.TOPIRAMATE, "Alternative: Helps with cravings and night eating"),
            ]
        else:
            # No specific symptoms - general weight loss focused
            priority_order = [
                (DrugName.WEGOVY, "First-line: Highest efficacy for weight loss (injectable)"),
                (DrugName.ZEPBOUND, "Alternative: Highest efficacy (injectable, dual GIP/GLP-1)"),
                (DrugName.SAXENDA, "Alternative: GLP-1 agonist for metabolic benefits (injectable)"),
                (DrugName.QSYMIA, "Alternative: Oral option with good efficacy"),
                (DrugName.PHENTERMINE, "Cost-effective oral option"),
                (DrugName.CONTRAVE, "Oral option for general weight loss"),
            ]

        # Filter to only include drugs still in the pool
        for drug, reasoning in priority_order:
            if drug in drug_pool:
                recommendations.append({
                    "medication": drug,
                    "priority": len(recommendations) + 1,
                    "reasoning": reasoning
                })

        # Add remaining drugs from pool that weren't prioritized
        for drug in drug_pool:
            if not any(r["medication"] == drug for r in recommendations):
                recommendations.append({
                    "medication": drug,
                    "priority": len(recommendations) + 1,
                    "reasoning": "Alternative option"
                })

        return recommendations

    @staticmethod
    def add_special_considerations(
        recommendations: List[Dict[str, Any]],
        health_conditions: List[str]
    ) -> List[str]:
        """Add warnings and special considerations"""
        warnings = []

        # Check for special monitoring requirements
        if "controlled_hypertension" in health_conditions:
            warnings.append("⚠️ Blood pressure monitoring required during treatment")

        if "glaucoma_stable" in health_conditions:
            warnings.append("⚠️ Intraocular pressure monitoring required; ophthalmologist confirmation needed")

        if "cardiovascular_stable" in health_conditions:
            warnings.append("⚠️ Regular cardiac function monitoring required; cardiologist confirmation needed")

        if "thyroid_controlled" in health_conditions:
            warnings.append("⚠️ Continue thyroid monitoring during treatment")

        # Check for injectable medications
        if any(r["medication"] in [DrugName.WEGOVY, DrugName.ZEPBOUND] for r in recommendations):
            warnings.append("ℹ️ Wegovy and Zepbound are injectable medications")
            warnings.append("ℹ️ Exclude patients with history of pancreatitis for Wegovy/Zepbound")

        # Orlistat consideration
        if not recommendations or len(recommendations) == 0:
            warnings.append("ℹ️ Consider Orlistat if all other medications are contraindicated (note: significant GI side effects, requires low-fat diet)")

        return warnings

    def run_screening(self, questionnaire_data: Dict) -> Dict[str, Any]:
        """
        Main screening function - runs all 4 steps
        Returns complete screening results
        """
        result = {
            "is_eligible": False,
            "eligibility_message": "",
            "bmi": None,
            "bmi_category": None,
            "initial_drug_pool": [],
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

        # STEP I: Check basic eligibility
        is_eligible, eligibility_msg = self.check_eligibility(questionnaire_data)
        result["eligibility_message"] = eligibility_msg
        result["screening_steps"].append({
            "step": "I - Eligibility Check",
            "result": eligibility_msg
        })

        if not is_eligible:
            return result

        # STEP II: BMI-based eligibility
        bmi_eligible, bmi_category, initial_pool = self.determine_bmi_eligibility(
            bmi,
            questionnaire_data.get("comorbidities", [])
        )
        result["bmi_category"] = bmi_category
        result["initial_drug_pool"] = initial_pool
        result["screening_steps"].append({
            "step": "II - BMI Assessment",
            "result": f"{bmi_category}. Initial drug pool: {len(initial_pool)} medications"
        })

        if not bmi_eligible:
            result["eligibility_message"] = f"Temporarily ineligible: {bmi_category}. Prioritize lifestyle intervention."
            return result

        result["is_eligible"] = True

        # STEP III: Exclude contraindicated drugs
        remaining_drugs, excluded, special_notes = self.exclude_contraindicated_drugs(
            initial_pool,
            questionnaire_data.get("health_conditions", []),
            questionnaire_data
        )
        result["excluded_drugs"] = excluded
        result["screening_steps"].append({
            "step": "III - Contraindication Screening",
            "result": f"Excluded {len(excluded)} medications. Remaining: {len(remaining_drugs)}"
        })

        # Add special notes to warnings
        result["warnings"].extend(special_notes)

        # STEP IV: Prioritize by symptoms
        recommendations = self.prioritize_by_symptoms(
            remaining_drugs,
            questionnaire_data.get("symptoms", [])
        )
        result["recommended_drugs"] = recommendations
        result["screening_steps"].append({
            "step": "IV - Symptom-Based Prioritization",
            "result": f"Generated {len(recommendations)} prioritized recommendations"
        })

        # Add special considerations
        warnings = self.add_special_considerations(
            recommendations,
            questionnaire_data.get("health_conditions", [])
        )
        result["warnings"] = warnings

        return result
