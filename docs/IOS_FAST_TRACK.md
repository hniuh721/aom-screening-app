# iOS App - Fast Track (3-4 Hours)

## ⚡ Quick Version - Get It Working Fast!

This guide will help you build a **working iOS app in 3-4 hours**. We'll focus on core functionality and use simpler code patterns.

---

## 🎯 What You'll Build

- ✅ Basic questionnaire form (all 5 sections)
- ✅ API integration
- ✅ Results display
- ✅ Working navigation

**Time: 3-4 hours** (if you follow along step-by-step)

---

## 📋 Prerequisites (5 minutes)

1. **Xcode installed** (Mac App Store)
2. **Backend running:**
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn app.main:app --reload
   ```
3. **Test API:** Open http://localhost:8000/docs in browser

---

## 🚀 Step 1: Create Xcode Project (5 minutes)

1. Open **Xcode**
2. **File → New → Project**
3. Select **iOS → App**
4. Fill in:
   - **Product Name:** `AOMScreening`
   - **Interface:** `SwiftUI`
   - **Language:** `Swift`
5. **Save** and open project

---

## 🚀 Step 2: Add Models (15 minutes)

### Create `Models` folder:
1. Right-click project → **New Group** → Name it `Models`
2. Right-click `Models` → **New File** → **Swift File** → `Questionnaire.swift`

**Paste this code:**

```swift
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
    let eligibilityMessage: String
    let age: Int?
    let gender: String?
    let bmiCategory: String
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
```

---

## 🚀 Step 3: Add API Service (20 minutes)

### Create `Services` folder and `APIService.swift`:

```swift
import Foundation

class APIService {
    static let shared = APIService()
    private let baseURL = "http://localhost:8000/api"
    
    func createQuestionnaire(_ data: QuestionnaireCreate) async throws -> Questionnaire {
        guard let url = URL(string: "\(baseURL)/questionnaires/anonymous") else {
            throw URLError(.badURL)
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let encoder = JSONEncoder()
        encoder.keyEncodingStrategy = .convertToSnakeCase
        request.httpBody = try encoder.encode(data)
        
        let (data, _) = try await URLSession.shared.data(for: request)
        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        return try decoder.decode(Questionnaire.self, from: data)
    }
    
    func submitQuestionnaire(id: Int) async throws {
        guard let url = URL(string: "\(baseURL)/questionnaires/\(id)/submit") else {
            throw URLError(.badURL)
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        _ = try await URLSession.shared.data(for: request)
    }
    
    func runScreening(questionnaireId: Int) async throws -> ScreeningResult {
        guard let url = URL(string: "\(baseURL)/screening/run/\(questionnaireId)") else {
            throw URLError(.badURL)
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        let (data, _) = try await URLSession.shared.data(for: request)
        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        return try decoder.decode(ScreeningResult.self, from: data)
    }
    
    func getResults(questionnaireId: Int) async throws -> ScreeningResult {
        guard let url = URL(string: "\(baseURL)/screening/results/\(questionnaireId)") else {
            throw URLError(.badURL)
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "GET"
        
        let (data, _) = try await URLSession.shared.data(for: request)
        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        return try decoder.decode(ScreeningResult.self, from: data)
    }
}
```

---

## 🚀 Step 4: Update Info.plist (2 minutes)

**Important:** Allow localhost connections

1. Click on project in navigator
2. Select target → **Info** tab
3. Add new key: **App Transport Security Settings**
4. Add sub-key: **Allow Arbitrary Loads in Web Content** = `YES`
5. OR add: **Allow Local Networking** = `YES`

---

## 🚀 Step 5: Create Main View (60 minutes)

### Replace `ContentView.swift` with this:

```swift
import SwiftUI

struct ContentView: View {
    @State private var age = ""
    @State private var gender = "male"
    @State private var contactNumber = ""
    @State private var isChildbearingAgeWoman = false
    @State private var heightFt = ""
    @State private var heightIn = ""
    @State private var weightLb = ""
    
    @State private var eatingHabits: Set<String> = []
    @State private var healthConditions: Set<String> = []
    
    @State private var currentMedications = ""
    @State private var hasDrugAllergies = false
    @State private var drugAllergies = ""
    @State private var additionalRemarks = ""
    
    @State private var isLoading = false
    @State private var errorMessage: String?
    @State private var showResults = false
    @State private var questionnaireId: Int?
    @State private var screeningResult: ScreeningResult?
    
    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 20) {
                    // Section I: Basic Information
                    VStack(alignment: .leading, spacing: 12) {
                        Text("I. Basic Information")
                            .font(.title2)
                            .fontWeight(.bold)
                            .padding(.horizontal)
                        
                        Group {
                            TextField("Age *", text: $age)
                                .keyboardType(.numberPad)
                            TextField("Contact Number", text: $contactNumber)
                            
                            Picker("Gender", selection: $gender) {
                                Text("Male").tag("male")
                                Text("Female").tag("female")
                                Text("Other").tag("other")
                            }
                            
                            Toggle("Woman of childbearing age (18-49)?", isOn: $isChildbearingAgeWoman)
                            
                            HStack {
                                TextField("Height (ft)", text: $heightFt)
                                    .keyboardType(.numberPad)
                                TextField("Height (in)", text: $heightIn)
                                    .keyboardType(.numberPad)
                            }
                            
                            TextField("Weight (lb) *", text: $weightLb)
                                .keyboardType(.decimalPad)
                        }
                        .textFieldStyle(.roundedBorder)
                        .padding(.horizontal)
                    }
                    
                    // Section II: Eating Habits
                    VStack(alignment: .leading, spacing: 12) {
                        Text("II. Eating Habits & Feelings")
                            .font(.title2)
                            .fontWeight(.bold)
                            .padding(.horizontal)
                        
                        let habits = [
                            ("excessive_appetite", "Often feel very hungry"),
                            ("lack_of_satiety", "Don't feel full after eating"),
                            ("binge_eating", "Eat a lot quickly"),
                            ("emotional_eating", "Eat more when stressed"),
                            ("night_eating", "Eat before bed or at night"),
                            ("frequent_snacking", "Often eat snacks"),
                            ("none", "None of the above")
                        ]
                        
                        ForEach(habits, id: \.0) { habit in
                            Toggle(habit.1, isOn: Binding(
                                get: { eatingHabits.contains(habit.0) },
                                set: { if $0 { eatingHabits.insert(habit.0) } else { eatingHabits.remove(habit.0) } }
                            ))
                            .padding(.horizontal)
                        }
                    }
                    
                    // Section III: Medical Conditions
                    VStack(alignment: .leading, spacing: 12) {
                        Text("III. Medical Conditions")
                            .font(.title2)
                            .fontWeight(.bold)
                            .padding(.horizontal)
                        
                        let conditions = [
                            ("hypertension", "Hypertension"),
                            ("diabetes", "Type 2 Diabetes"),
                            ("sleep_apnea", "Sleep Apnea"),
                            ("heart_disease", "Heart Disease"),
                            ("adhd", "ADD/ADHD"),
                            ("none", "No conditions")
                        ]
                        
                        ForEach(conditions, id: \.0) { condition in
                            Toggle(condition.1, isOn: Binding(
                                get: { healthConditions.contains(condition.0) },
                                set: { if $0 { healthConditions.insert(condition.0) } else { healthConditions.remove(condition.0) } }
                            ))
                            .padding(.horizontal)
                        }
                    }
                    
                    // Section IV: Medications
                    VStack(alignment: .leading, spacing: 12) {
                        Text("IV. Medications & Allergies")
                            .font(.title2)
                            .fontWeight(.bold)
                            .padding(.horizontal)
                        
                        TextField("Current Medications", text: $currentMedications, axis: .vertical)
                            .textFieldStyle(.roundedBorder)
                            .lineLimit(3...6)
                            .padding(.horizontal)
                        
                        Toggle("Has Drug Allergies?", isOn: $hasDrugAllergies)
                            .padding(.horizontal)
                        
                        if hasDrugAllergies {
                            TextField("List allergies", text: $drugAllergies, axis: .vertical)
                                .textFieldStyle(.roundedBorder)
                                .lineLimit(2...4)
                                .padding(.horizontal)
                        }
                    }
                    
                    // Section V: Additional Remarks
                    VStack(alignment: .leading, spacing: 12) {
                        Text("V. Additional Remarks")
                            .font(.title2)
                            .fontWeight(.bold)
                            .padding(.horizontal)
                        
                        TextField("Additional information", text: $additionalRemarks, axis: .vertical)
                            .textFieldStyle(.roundedBorder)
                            .lineLimit(3...6)
                            .padding(.horizontal)
                    }
                    
                    // Submit Button
                    Button(action: submitForm) {
                        if isLoading {
                            ProgressView()
                                .frame(maxWidth: .infinity)
                                .frame(height: 50)
                        } else {
                            Text("Submit Questionnaire")
                                .frame(maxWidth: .infinity)
                                .frame(height: 50)
                        }
                    }
                    .buttonStyle(.borderedProminent)
                    .disabled(isLoading)
                    .padding(.horizontal)
                    
                    if let error = errorMessage {
                        Text(error)
                            .foregroundColor(.red)
                            .padding()
                    }
                }
                .padding(.vertical)
            }
            .navigationTitle("AOM Screening")
            .sheet(isPresented: $showResults) {
                if let result = screeningResult {
                    ResultsView(result: result)
                }
            }
        }
    }
    
    func submitForm() {
        guard let ageInt = Int(age),
              let heightFtInt = Int(heightFt),
              let heightInInt = Int(heightIn),
              let weightLbDouble = Double(weightLb) else {
            errorMessage = "Please fill all required fields"
            return
        }
        
        isLoading = true
        errorMessage = nil
        
        Task {
            do {
                let questionnaire = QuestionnaireCreate(
                    age: ageInt,
                    gender: gender,
                    contactNumber: contactNumber.isEmpty ? nil : contactNumber,
                    isChildbearingAgeWoman: isChildbearingAgeWoman,
                    heightFt: heightFtInt,
                    heightIn: heightInInt,
                    weightLb: weightLbDouble,
                    eatingHabits: Array(eatingHabits),
                    healthConditions: Array(healthConditions),
                    currentMedications: currentMedications.isEmpty ? [] : [currentMedications],
                    hasDrugAllergies: hasDrugAllergies,
                    drugAllergies: drugAllergies.isEmpty ? [] : drugAllergies.split(separator: ",").map { String($0.trimmingCharacters(in: .whitespaces)) },
                    additionalRemarks: additionalRemarks.isEmpty ? nil : additionalRemarks
                )
                
                let created = try await APIService.shared.createQuestionnaire(questionnaire)
                guard let id = created.id else { return }
                
                try await APIService.shared.submitQuestionnaire(id: id)
                let result = try await APIService.shared.runScreening(questionnaireId: id)
                
                await MainActor.run {
                    screeningResult = result
                    showResults = true
                    isLoading = false
                }
            } catch {
                await MainActor.run {
                    errorMessage = "Error: \(error.localizedDescription)"
                    isLoading = false
                }
            }
        }
    }
}
```

---

## 🚀 Step 6: Create Results View (20 minutes)

### Create new Swift file: `ResultsView.swift`

```swift
import SwiftUI

struct ResultsView: View {
    let result: ScreeningResult
    @Environment(\.dismiss) var dismiss
    
    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 20) {
                    // Header
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Screening Results")
                            .font(.largeTitle)
                            .fontWeight(.bold)
                        
                        Text(result.eligibilityMessage)
                            .foregroundColor(.secondary)
                    }
                    .padding()
                    
                    // Patient Info
                    VStack(alignment: .leading, spacing: 8) {
                        if let age = result.age {
                            InfoRow(label: "Age", value: "\(age) years")
                        }
                        if let gender = result.gender {
                            InfoRow(label: "Gender", value: gender.capitalized)
                        }
                        InfoRow(label: "BMI", value: result.bmiCategory)
                    }
                    .padding()
                    .background(Color(.systemGray6))
                    .cornerRadius(10)
                    .padding(.horizontal)
                    
                    // Warnings
                    if !result.warnings.isEmpty {
                        VStack(alignment: .leading, spacing: 8) {
                            Text("Important Warnings")
                                .font(.headline)
                            ForEach(result.warnings, id: \.self) { warning in
                                Text("• \(warning)")
                                    .font(.subheadline)
                            }
                        }
                        .padding()
                        .background(Color.orange.opacity(0.2))
                        .cornerRadius(10)
                        .padding(.horizontal)
                    }
                    
                    // Recommended Medications
                    VStack(alignment: .leading, spacing: 12) {
                        Text("Recommended Medications")
                            .font(.title2)
                            .fontWeight(.bold)
                            .padding(.horizontal)
                        
                        ForEach(result.recommendedDrugs, id: \.medication) { drug in
                            VStack(alignment: .leading, spacing: 4) {
                                Text(drug.medication)
                                    .font(.headline)
                                    .foregroundColor(.blue)
                                Text(drug.reasoning)
                                    .font(.subheadline)
                                    .foregroundColor(.secondary)
                            }
                            .padding()
                            .frame(maxWidth: .infinity, alignment: .leading)
                            .background(Color(.systemGray6))
                            .cornerRadius(10)
                            .padding(.horizontal)
                        }
                    }
                    
                    // Next Steps
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Next Steps")
                            .font(.headline)
                        Text("1. A doctor will review your questionnaire")
                        Text("2. The doctor may contact you for consultation")
                        Text("3. Final medication selection will be made by your doctor")
                        Text("4. Do not start any medication without doctor's approval")
                            .fontWeight(.bold)
                    }
                    .font(.subheadline)
                    .padding()
                    .background(Color.yellow.opacity(0.2))
                    .cornerRadius(10)
                    .padding(.horizontal)
                }
                .padding(.vertical)
            }
            .navigationTitle("Results")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Done") {
                        dismiss()
                    }
                }
            }
        }
    }
}

struct InfoRow: View {
    let label: String
    let value: String
    
    var body: some View {
        HStack {
            Text(label)
                .foregroundColor(.secondary)
            Spacer()
            Text(value)
                .fontWeight(.semibold)
        }
    }
}
```

---

## 🚀 Step 7: Test It! (10 minutes)

1. **Build:** ⌘B (should succeed)
2. **Run:** ⌘R (select iPhone simulator)
3. **Fill form** with test data:
   - Age: 35
   - Gender: Female
   - Height: 5 ft, 4 in
   - Weight: 185 lb
   - Select some eating habits
   - Select some medical conditions
4. **Click Submit**
5. **Check Results** appear

---

## ⚠️ Troubleshooting

### "Cannot connect to localhost"
- Use your Mac's IP: `http://192.168.1.X:8000` instead of `localhost`
- Or use `127.0.0.1:8000`

### "Build failed"
- Clean: Product → Clean Build Folder (⇧⌘K)
- Check all files are added to target

### "API error"
- Make sure backend is running
- Check API URL in `APIService.swift`
- Test API in browser first: http://localhost:8000/docs

---

## ✅ You're Done!

**Total Time: 3-4 hours**

You now have a **working iOS app** that:
- ✅ Collects questionnaire data
- ✅ Sends to your backend API
- ✅ Displays screening results
- ✅ Works on iPhone simulator

---

## 🎨 Next Steps (Optional - Add Later)

- [ ] Polish UI (match your HTML mockup)
- [ ] Add more form validation
- [ ] Add loading animations
- [ ] Add error handling UI
- [ ] Test on physical device
- [ ] Add app icon

**But you have a working app now!** 🎉

