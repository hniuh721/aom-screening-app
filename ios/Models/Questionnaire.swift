import Foundation

struct QuestionnaireCreate: Codable {
    let age: Int
    let gender: String
    let contactNumber: String?
    let isChildbearingAgeWoman: Bool
    let heightFt: Int
    let heightIn: Int
    let weightLb: Double
    let eatingHabits: [String]
    let healthConditions: [String]
    let currentMedications: [String]
    let hasDrugAllergies: Bool
    let drugAllergies: [String]
    let additionalRemarks: String?
    
    enum CodingKeys: String, CodingKey {
        case age, gender
        case contactNumber = "contact_number"
        case isChildbearingAgeWoman = "is_childbearing_age_woman"
        case heightFt = "height_ft"
        case heightIn = "height_in"
        case weightLb = "weight_lb"
        case eatingHabits = "eating_habits"
        case healthConditions = "health_conditions"
        case currentMedications = "current_medications"
        case hasDrugAllergies = "has_drug_allergies"
        case drugAllergies = "drug_allergies"
        case additionalRemarks = "additional_remarks"
    }
}

struct Questionnaire: Codable {
    let id: Int?
}

struct ScreeningResult: Codable {
    let id: Int
    let questionnaireId: Int
    let isEligible: Bool
    let eligibilityMessage: String?
    let age: Int?
    let gender: String?
    let bmiCategory: String?
    let recommendedDrugs: [MedicationRecommendation]
    let warnings: [String]
    
    enum CodingKeys: String, CodingKey {
        case id
        case questionnaireId = "questionnaire_id"
        case isEligible = "is_eligible"
        case eligibilityMessage = "eligibility_message"
        case age, gender
        case bmiCategory = "bmi_category"
        case recommendedDrugs = "recommended_drugs"
        case warnings
    }
}

struct MedicationRecommendation: Codable {
    let medication: String
    let priority: Int
    let reasoning: String
}
