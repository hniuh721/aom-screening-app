# BMI Eligibility Workflow for Oral Anti-Obesity Medications (AOMs)

## Overview
This document describes the BMI-based eligibility screening workflow implemented in the AOM screening application.

---

## 🚦 Eligibility Gate: BMI Threshold

### **Critical Rule: BMI < 27 = Immediate Ineligibility**

The application implements a **mandatory BMI eligibility gate** as the first screening step:

```
┌─────────────────────────────────────┐
│   Patient Submits Questionnaire     │
└──────────────┬──────────────────────┘
               │
               ▼
        ┌──────────────┐
        │ Calculate BMI │
        └──────┬───────┘
               │
               ▼
        ┌──────────────┐
        │  BMI < 27?   │
        └──────┬───────┘
               │
        ┌──────┴──────┐
        │             │
       YES           NO
        │             │
        ▼             ▼
  ⛔ NOT ELIGIBLE   ✅ PROCEED TO SCREENING
  Skip all further  │
  assessments       ├─> Comorbidity Assessment
                    ├─> Contraindication Screening
                    └─> Medication Recommendations
```

---

## 📋 Detailed Workflow

### **Step 1: BMI Calculation**
- Input: Height (feet, inches) and Weight (pounds)
- Calculation: BMI = weight(kg) / height(m)²
- Output: Numeric BMI value (e.g., 26.5, 31.2)

### **Step 2: BMI Eligibility Gate**

#### **Scenario A: BMI < 27**
**Result:** ⛔ **NOT ELIGIBLE**

**System Actions:**
1. ✅ Set `is_eligible = false`
2. ✅ Set eligibility message: "Not eligible for oral anti-obesity medications"
3. ✅ **Skip ALL subsequent assessments:**
   - ❌ No comorbidity evaluation
   - ❌ No contraindication screening
   - ❌ No medication recommendations
4. ✅ Display ineligibility notice with:
   - Clear explanation of BMI requirements
   - Current BMI value
   - Lifestyle modification recommendations
   - Alternative next steps

**Patient Message:**
```
⛔ BMI Requirement Not Met: Your BMI is below 27.

Oral anti-obesity medications are indicated for individuals with:
• BMI ≥ 30, OR
• BMI ≥ 27 with weight-related comorbidities
  (e.g., hypertension, diabetes, sleep apnea)

Your BMI: [calculated value]

💡 Recommendation: Focus on lifestyle modifications including
diet and exercise. Please consult with your healthcare provider
for personalized weight management strategies.
```

#### **Scenario B: BMI ≥ 27**
**Result:** ✅ **PROCEED TO FULL SCREENING**

**System Actions:**
1. ✅ Pass BMI eligibility gate
2. ✅ Log: "BMI ≥ 27: Passed eligibility gate. Proceeding to comorbidity assessment."
3. ✅ Continue to **Step 3: Comorbidity Assessment**
4. ✅ Continue to **Step 4: Contraindication Screening (Table 1)**
5. ✅ Continue to **Step 5: Medication Prioritization**

---

## 🎯 Clinical Rationale

### FDA and Clinical Guidelines
Oral anti-obesity medications are FDA-approved for:
- **BMI ≥ 30** (obesity), **OR**
- **BMI ≥ 27** (overweight) **with at least one weight-related comorbidity**

### Why BMI 27 as the Hard Cutoff?
- Below BMI 27, patients do not meet minimum criteria even WITH comorbidities
- BMI 27-29.9 patients require comorbidity documentation for eligibility
- BMI ≥ 30 patients are eligible regardless of comorbidities

### Efficiency Rationale
- **Avoids unnecessary processing** for clearly ineligible patients
- **Saves computational resources** by early exit
- **Provides faster feedback** to patients
- **Reduces clinician review burden** by not presenting ineligible cases

---

## 💻 Technical Implementation

### Backend Logic
**File:** `/backend/app/services/screening_service.py`

```python
def run_screening(self, questionnaire_data: Dict) -> Dict[str, Any]:
    # Calculate BMI
    bmi = self.calculate_bmi(
        questionnaire_data["height_ft"],
        questionnaire_data["height_in"],
        questionnaire_data["weight_lb"]
    )

    # ⛔ ELIGIBILITY GATE: BMI < 27 = immediate ineligibility
    if bmi < 27:
        result["is_eligible"] = False
        result["eligibility_message"] = "Not eligible for oral anti-obesity medications"
        # Skip all further screening
        return result

    # BMI ≥ 27: Proceed with normal screening workflow
    # ... continue with contraindication screening ...
```

### Frontend Display
**File:** `/frontend/src/pages/ScreeningResults.tsx`

The results page now has two distinct views:

**View 1: Ineligible (BMI < 27)**
- Red alert box with ineligibility notice
- Clear explanation of BMI requirements
- Display patient's actual BMI
- Lifestyle modification recommendations
- Alternative next steps (dietitian, exercise, reassessment)

**View 2: Eligible (BMI ≥ 27)**
- Normal screening results
- Contraindication sections (ABSOLUTE/RELATIVE)
- Medication recommendations
- Next steps for doctor review

---

## 📊 Example Scenarios

### Example 1: BMI 25.8
```
Patient: Female, 5'4", 150 lbs
Calculated BMI: 25.8

Result: ⛔ NOT ELIGIBLE
Comorbidities checked: Hypertension, Diabetes
Medications screened: NONE (skipped)

Message: "Your BMI is 25.8, which is below the minimum
requirement of 27. Focus on lifestyle modifications."
```

### Example 2: BMI 28.3 with Hypertension
```
Patient: Male, 5'10", 195 lbs
Calculated BMI: 28.0

Result: ✅ ELIGIBLE - Proceed to Screening
Comorbidities: Hypertension (well-controlled)
Screening performed: Yes
Medications: Wegovy, Zepbound recommended
             Phentermine/Vyvanse flagged (RELATIVE - hypertension)
```

### Example 3: BMI 32.1
```
Patient: Female, 5'6", 200 lbs
Calculated BMI: 32.3

Result: ✅ ELIGIBLE - Proceed to Screening
Comorbidities: None reported
Screening performed: Yes
Medications: All medications passed screening
             Prioritized by eating habits
```

---

## 🔄 Edge Cases & Special Considerations

### BMI Exactly 27.0
- **Treated as ELIGIBLE** (≥ 27 includes 27.0)
- Proceeds to full screening workflow
- Requires comorbidity documentation for insurance approval

### Borderline Cases (BMI 26.8-27.2)
- **No special handling in algorithm**
- BMI < 27.0 → Ineligible (hard cutoff)
- BMI ≥ 27.0 → Eligible (proceeds to screening)
- **Clinical consideration:** Doctor may reassess measurements if borderline

### Patient Asks for Exception
- **System does NOT override BMI gate**
- Hard-coded eligibility threshold
- Doctor must document medical necessity separately if considering off-label use
- Insurance unlikely to approve BMI < 27 even with comorbidities

---

## ⚕️ Provider Guidance

### When Patient is Ineligible (BMI < 27)

**Recommended Actions:**
1. ✅ Verify height/weight measurements are accurate
2. ✅ Counsel on lifestyle modifications:
   - Dietary changes (500-750 calorie deficit)
   - Physical activity (150+ min/week moderate intensity)
   - Behavioral strategies (food diary, portion control)
3. ✅ Refer to:
   - Registered dietitian for nutrition counseling
   - Exercise physiologist for activity planning
   - Behavioral health if emotional eating present
4. ✅ Schedule follow-up reassessment in 3-6 months
5. ✅ Document weight management goals and plan

**Insurance Considerations:**
- AOMs are typically NOT covered for BMI < 27
- Even with prior authorization, approval is unlikely
- Focus on covered lifestyle interventions

### When Patient is Eligible (BMI ≥ 27)

**For BMI 27-29.9:**
- ✅ Document weight-related comorbidities clearly
- ✅ Specify control status (controlled vs uncontrolled)
- ✅ Required for insurance approval

**For BMI ≥ 30:**
- ✅ Eligible regardless of comorbidities
- ✅ Proceed to contraindication screening
- ✅ Insurance typically covers with step therapy

---

## 📝 Documentation Requirements

### In Medical Record
For patients with BMI < 27:
```
Assessment: BMI [value] - below threshold for pharmacotherapy
Plan: Lifestyle modifications including dietary counseling
and exercise program. Reassess in 3-6 months.
```

For patients with BMI ≥ 27:
```
Assessment: BMI [value] - eligible for anti-obesity medication
Screening: Completed AOM screening questionnaire
Results: [List contraindications and recommendations]
Plan: Discussed medication options, risks, benefits...
```

---

## 🔧 System Maintenance

### If Threshold Changes
If clinical guidelines change the BMI threshold:

1. Update backend logic in `screening_service.py:299`:
   ```python
   if bmi < NEW_THRESHOLD:  # Change from 27
   ```

2. Update frontend messages in `ScreeningResults.tsx`

3. Update this documentation

4. Notify all clinicians of policy change

### Logging & Analytics
System logs BMI eligibility decisions:
- Track percentage of patients excluded at BMI gate
- Monitor average BMI of screened patients
- Identify trends in patient population

---

## ✅ Summary

**Key Points:**
1. ⛔ BMI < 27 = Immediate ineligibility, no further screening
2. ✅ BMI ≥ 27 = Eligible, proceed to full contraindication screening
3. 🚀 Early exit saves processing time and resources
4. 📋 Clear patient communication about eligibility criteria
5. ⚕️ Provider guidance for both eligible and ineligible patients

**Benefits:**
- Efficient screening workflow
- Clear eligibility determination
- Appropriate patient expectations
- Insurance-aligned criteria
- Evidence-based threshold

---

**Version:** 1.0
**Last Updated:** 2025-11-21
**Implementation Status:** ✅ Complete
