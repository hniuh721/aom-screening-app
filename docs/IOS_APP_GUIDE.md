# iOS App Development Guide - AOM Screening App

## 🎯 Overview

This guide will help you build a native iOS app for the AOM (Anti-Obesity Medication) Screening application. Your backend API is already set up and ready to use!

## 📋 Table of Contents

1. [Technology Stack Options](#technology-stack-options)
2. [Recommended Approach: SwiftUI](#recommended-approach-swiftui)
3. [Prerequisites](#prerequisites)
4. [Project Setup](#project-setup)
5. [Architecture & Structure](#architecture--structure)
6. [Implementation Steps](#implementation-steps)
7. [API Integration](#api-integration)
8. [Testing](#testing)
9. [Deployment](#deployment)

---

## 🛠 Technology Stack Options

### Option 1: Native iOS (SwiftUI) ⭐ **RECOMMENDED**
- **Pros:**
  - Best performance and native feel
  - Full access to iOS features
  - Best user experience
  - Apple's modern framework
  - Easy to maintain
  
- **Cons:**
  - iOS only (no Android)
  - Requires Mac and Xcode

### Option 2: React Native
- **Pros:**
  - Cross-platform (iOS + Android)
  - Reuse web code
  - Large community
  
- **Cons:**
  - Less native feel
  - Performance overhead
  - More complex setup

### Option 3: Flutter
- **Pros:**
  - Cross-platform
  - Good performance
  
- **Cons:**
  - Different language (Dart)
  - Less iOS-native feel

**Recommendation:** Use **SwiftUI** for the best iOS experience, especially since you already have the HTML mockup as a design reference.

---

## ✅ Prerequisites

Before starting, make sure you have:

1. **Mac computer** (required for iOS development)
2. **Xcode 15+** (free from Mac App Store)
3. **Apple Developer Account** (free for development, $99/year for App Store)
4. **iOS 17+** device or simulator for testing
5. **Backend API running** (your FastAPI server)

---

## 🚀 Project Setup

### Step 1: Create New Xcode Project

1. Open **Xcode**
2. Click **"Create a new Xcode project"**
3. Select **"iOS"** → **"App"**
4. Fill in:
   - **Product Name:** `AOMScreening`
   - **Interface:** `SwiftUI`
   - **Language:** `Swift`
   - **Storage:** `None` (we'll use API)
5. Choose save location
6. Click **"Create"**

### Step 2: Project Structure

Create this folder structure in your Xcode project:

```
AOMScreening/
├── App/
│   └── AOMScreeningApp.swift          # Main app entry
├── Models/
│   ├── Questionnaire.swift
│   ├── ScreeningResult.swift
│   └── User.swift
├── Views/
│   ├── Questionnaire/
│   │   ├── QuestionnaireView.swift
│   │   ├── BasicInfoView.swift
│   │   ├── EatingHabitsView.swift
│   │   ├── MedicalConditionsView.swift
│   │   ├── MedicationsView.swift
│   │   └── AdditionalRemarksView.swift
│   ├── Results/
│   │   └── ResultsView.swift
│   └── Components/
│       ├── IOSCard.swift
│       ├── IOSButton.swift
│       ├── IOSSwitch.swift
│       └── IOSSegmentedControl.swift
├── ViewModels/
│   ├── QuestionnaireViewModel.swift
│   └── ResultsViewModel.swift
├── Services/
│   ├── APIService.swift
│   └── NetworkManager.swift
└── Utilities/
    ├── Constants.swift
    └── Extensions.swift
```

---

## 🏗 Architecture & Structure

### Recommended Architecture: MVVM (Model-View-ViewModel)

```
┌─────────────┐
│    Views     │  (SwiftUI Views - UI only)
└──────┬───────┘
       │
       ▼
┌─────────────┐
│ ViewModels  │  (Business logic, state management)
└──────┬───────┘
       │
       ▼
┌─────────────┐
│   Services  │  (API calls, network)
└──────┬───────┘
       │
       ▼
┌─────────────┐
│   Models    │  (Data structures)
└─────────────┘
```

---

## 📝 Implementation Steps

### Phase 1: Setup & Models (Day 1)

#### 1.1 Create Models

**Models/Questionnaire.swift:**
```swift
import Foundation

struct Questionnaire: Codable {
    let id: Int?
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
        case id
        case age
        case gender
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
```

**Models/ScreeningResult.swift:**
```swift
import Foundation

struct ScreeningResult: Codable {
    let id: Int
    let questionnaireId: Int
    let isEligible: Bool
    let eligibilityMessage: String
    let age: Int?
    let gender: String?
    let isChildbearingAgeWoman: Bool?
    let bmiCategory: String
    let recommendedDrugs: [MedicationRecommendation]
    let warnings: [String]
    let screeningLogic: [ScreeningStep]
    
    enum CodingKeys: String, CodingKey {
        case id
        case questionnaireId = "questionnaire_id"
        case isEligible = "is_eligible"
        case eligibilityMessage = "eligibility_message"
        case age, gender
        case isChildbearingAgeWoman = "is_childbearing_age_woman"
        case bmiCategory = "bmi_category"
        case recommendedDrugs = "recommended_drugs"
        case warnings
        case screeningLogic = "screening_logic"
    }
}

struct MedicationRecommendation: Codable {
    let medication: String
    let priority: Int
    let reasoning: String
}

struct ScreeningStep: Codable {
    let step: String
    let result: String
}
```

#### 1.2 Create Constants

**Utilities/Constants.swift:**
```swift
import Foundation

struct Constants {
    static let apiBaseURL = "http://localhost:8000/api"
    // For production: "https://your-api-domain.com/api"
    
    // API Endpoints
    struct Endpoints {
        static let createQuestionnaire = "/questionnaires/anonymous"
        static let submitQuestionnaire = "/questionnaires/%d/submit"
        static let runScreening = "/screening/run/%d"
        static let getResults = "/screening/results/%d"
    }
    
    // Form Options
    struct EatingHabits {
        static let all = [
            "excessive_appetite",
            "lack_of_satiety",
            "binge_eating",
            "emotional_eating",
            "night_eating",
            "frequent_snacking",
            "none"
        ]
        
        static let labels: [String: String] = [
            "excessive_appetite": "Often feel very hungry and hard to control how much I eat",
            "lack_of_satiety": "Don't feel full after eating, and get hungry again soon",
            "binge_eating": "Sometimes eat a lot of food quickly and can't stop myself",
            "emotional_eating": "Eat more when I'm anxious, sad, stressed, or in other mood swings",
            "night_eating": "Eat a lot within 2 hours before bed, or wake up to eat at night",
            "frequent_snacking": "Often eat snacks between regular meals",
            "none": "None of the above situations"
        ]
    }
    
    struct HealthConditions {
        static let all = [
            "hypertension",
            "dyslipidemia",
            "coronary_artery_disease",
            "diabetes",
            "sleep_apnea",
            "arthritis",
            "gerd",
            "recurrent_kidney_stones",
            "glaucoma",
            "history_stroke",
            "heart_disease",
            "intracranial_hypertension",
            "adhd",
            "psychiatric_treatment",
            "thyroid_cancer",
            "history_pancreatitis",
            "gastroparesis",
            "taking_tamoxifen",
            "pregnancy_breastfeeding",
            "planning_pregnancy",
            "history_drug_abuse",
            "hyperthyroidism",
            "none"
        ]
        
        static let labels: [String: String] = [
            "hypertension": "Hypertension",
            "dyslipidemia": "Dyslipidemia (HDL < 50 mg/dL for women, HDL < 40 mg/dL for men)",
            "coronary_artery_disease": "Coronary Artery Disease (CAD)",
            "diabetes": "Type 2 Diabetes Mellitus (DM2)",
            "sleep_apnea": "Obstructive Sleep Apnea (OSA)",
            "arthritis": "Symptomatic arthritis of lower extremities",
            "gerd": "Gastroesophageal Reflux Disease (GERD)",
            "recurrent_kidney_stones": "Recurrent kidney stones",
            "glaucoma": "Glaucoma",
            "history_stroke": "Stroke",
            "heart_disease": "Cardiovascular disease",
            "intracranial_hypertension": "Intracranial hypertension",
            "adhd": "ADD/ADHD",
            "psychiatric_treatment": "Psychiatric disorders",
            "thyroid_cancer": "Medullary thyroid cancer",
            "history_pancreatitis": "Pancreatitis",
            "gastroparesis": "Gastroparesis",
            "taking_tamoxifen": "Currently taking Tamoxifen",
            "pregnancy_breastfeeding": "Currently pregnant",
            "planning_pregnancy": "Planning to become pregnant within 3 months",
            "history_drug_abuse": "History of substance abuse",
            "hyperthyroidism": "Thyroid dysfunction",
            "none": "No above underlying medical conditions"
        ]
    }
}
```

---

### Phase 2: API Service (Day 2)

#### 2.1 Create Network Manager

**Services/NetworkManager.swift:**
```swift
import Foundation

enum NetworkError: Error {
    case invalidURL
    case noData
    case decodingError
    case serverError(Int)
    case unknown(Error)
}

class NetworkManager {
    static let shared = NetworkManager()
    
    private let session: URLSession
    private let baseURL: String
    
    init(baseURL: String = Constants.apiBaseURL) {
        self.baseURL = baseURL
        let config = URLSessionConfiguration.default
        config.timeoutIntervalForRequest = 30
        self.session = URLSession(configuration: config)
    }
    
    func request<T: Decodable>(
        endpoint: String,
        method: String = "GET",
        body: Encodable? = nil
    ) async throws -> T {
        guard let url = URL(string: baseURL + endpoint) else {
            throw NetworkError.invalidURL
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = method
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        if let body = body {
            let encoder = JSONEncoder()
            encoder.keyEncodingStrategy = .convertToSnakeCase
            request.httpBody = try encoder.encode(body)
        }
        
        let (data, response) = try await session.data(for: request)
        
        if let httpResponse = response as? HTTPURLResponse {
            if httpResponse.statusCode >= 400 {
                throw NetworkError.serverError(httpResponse.statusCode)
            }
        }
        
        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        
        do {
            return try decoder.decode(T.self, from: data)
        } catch {
            print("Decoding error: \(error)")
            throw NetworkError.decodingError
        }
    }
}
```

#### 2.2 Create API Service

**Services/APIService.swift:**
```swift
import Foundation

class APIService {
    static let shared = APIService()
    private let networkManager = NetworkManager.shared
    
    // MARK: - Questionnaires
    
    func createQuestionnaire(_ questionnaire: QuestionnaireCreate) async throws -> Questionnaire {
        return try await networkManager.request(
            endpoint: Constants.Endpoints.createQuestionnaire,
            method: "POST",
            body: questionnaire
        )
    }
    
    func submitQuestionnaire(id: Int) async throws -> Questionnaire {
        let endpoint = String(format: Constants.Endpoints.submitQuestionnaire, id)
        return try await networkManager.request(
            endpoint: endpoint,
            method: "POST"
        )
    }
    
    // MARK: - Screening
    
    func runScreening(questionnaireId: Int) async throws -> ScreeningResult {
        let endpoint = String(format: Constants.Endpoints.runScreening, questionnaireId)
        return try await networkManager.request(
            endpoint: endpoint,
            method: "POST"
        )
    }
    
    func getScreeningResults(questionnaireId: Int) async throws -> ScreeningResult {
        let endpoint = String(format: Constants.Endpoints.getResults, questionnaireId)
        return try await networkManager.request(
            endpoint: endpoint,
            method: "GET"
        )
    }
}
```

---

### Phase 3: ViewModels (Day 3)

#### 3.1 Questionnaire ViewModel

**ViewModels/QuestionnaireViewModel.swift:**
```swift
import Foundation
import SwiftUI

@MainActor
class QuestionnaireViewModel: ObservableObject {
    @Published var age: String = ""
    @Published var gender: String = "male"
    @Published var contactNumber: String = ""
    @Published var isChildbearingAgeWoman: Bool = false
    @Published var heightFt: String = ""
    @Published var heightIn: String = ""
    @Published var weightLb: String = ""
    
    @Published var eatingHabits: Set<String> = []
    @Published var healthConditions: Set<String> = []
    
    @Published var currentMedications: String = ""
    @Published var hasDrugAllergies: Bool = false
    @Published var drugAllergies: String = ""
    @Published var additionalRemarks: String = ""
    
    @Published var isLoading: Bool = false
    @Published var errorMessage: String?
    @Published var questionnaireId: Int?
    
    private let apiService = APIService.shared
    
    func toggleEatingHabit(_ habit: String) {
        if eatingHabits.contains(habit) {
            eatingHabits.remove(habit)
        } else {
            eatingHabits.insert(habit)
        }
    }
    
    func toggleHealthCondition(_ condition: String) {
        if healthConditions.contains(condition) {
            healthConditions.remove(condition)
        } else {
            healthConditions.insert(condition)
        }
    }
    
    func submitQuestionnaire() async {
        isLoading = true
        errorMessage = nil
        
        guard let ageInt = Int(age),
              let heightFtInt = Int(heightFt),
              let heightInInt = Int(heightIn),
              let weightLbDouble = Double(weightLb) else {
            errorMessage = "Please fill in all required fields"
            isLoading = false
            return
        }
        
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
        
        do {
            let created = try await apiService.createQuestionnaire(questionnaire)
            self.questionnaireId = created.id
            
            // Submit questionnaire
            _ = try await apiService.submitQuestionnaire(id: created.id!)
            
            // Run screening
            _ = try await apiService.runScreening(questionnaireId: created.id!)
            
        } catch {
            errorMessage = "Failed to submit questionnaire: \(error.localizedDescription)"
        }
        
        isLoading = false
    }
}
```

---

### Phase 4: Views (Days 4-6)

#### 4.1 Main Questionnaire View

**Views/Questionnaire/QuestionnaireView.swift:**
```swift
import SwiftUI

struct QuestionnaireView: View {
    @StateObject private var viewModel = QuestionnaireViewModel()
    @State private var showResults = false
    
    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 16) {
                    // Instructions Alert
                    AlertCard(
                        type: .info,
                        title: "Instructions",
                        message: "All questions must be answered truthfully. False information may lead to incorrect medication selection."
                    )
                    
                    // Section I: Basic Information
                    BasicInfoView(viewModel: viewModel)
                    
                    // Section II: Eating Habits
                    EatingHabitsView(viewModel: viewModel)
                    
                    // Section III: Medical Conditions
                    MedicalConditionsView(viewModel: viewModel)
                    
                    // Section IV: Medications
                    MedicationsView(viewModel: viewModel)
                    
                    // Section V: Additional Remarks
                    AdditionalRemarksView(viewModel: viewModel)
                    
                    // Submit Button
                    Button(action: {
                        Task {
                            await viewModel.submitQuestionnaire()
                            if viewModel.questionnaireId != nil {
                                showResults = true
                            }
                        }
                    }) {
                        if viewModel.isLoading {
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
                    .disabled(viewModel.isLoading)
                    .padding(.horizontal)
                    
                    if let error = viewModel.errorMessage {
                        Text(error)
                            .foregroundColor(.red)
                            .padding()
                    }
                }
                .padding(.vertical)
            }
            .navigationTitle("AOM Screening")
            .navigationBarTitleDisplayMode(.large)
            .sheet(isPresented: $showResults) {
                if let id = viewModel.questionnaireId {
                    ResultsView(questionnaireId: id)
                }
            }
        }
    }
}
```

#### 4.2 Create iOS-Style Components

**Views/Components/IOSCard.swift:**
```swift
import SwiftUI

struct IOSCard<Content: View>: View {
    let title: String?
    let subtitle: String?
    let content: Content
    
    init(title: String? = nil, subtitle: String? = nil, @ViewBuilder content: () -> Content) {
        self.title = title
        self.subtitle = subtitle
        self.content = content()
    }
    
    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            if let title = title {
                VStack(alignment: .leading, spacing: 4) {
                    Text(title)
                        .font(.title2)
                        .fontWeight(.bold)
                    if let subtitle = subtitle {
                        Text(subtitle)
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                    }
                }
                .padding()
                .frame(maxWidth: .infinity, alignment: .leading)
                .background(Color(.systemGray6))
            }
            
            content
                .padding()
        }
        .background(Color(.systemBackground))
        .cornerRadius(10)
        .shadow(color: Color.black.opacity(0.1), radius: 5, x: 0, y: 2)
    }
}
```

Continue with other components and views following the same pattern...

---

## 🔌 API Integration Checklist

- [ ] Test API connectivity
- [ ] Handle network errors gracefully
- [ ] Add loading states
- [ ] Implement error handling
- [ ] Add retry logic for failed requests
- [ ] Cache responses if needed

---

## 🧪 Testing

### Unit Tests
- Test ViewModels
- Test API Service
- Test Models

### UI Tests
- Test form submission
- Test navigation
- Test error handling

### Manual Testing
- Test on iPhone simulator
- Test on physical device
- Test with slow network
- Test with API offline

---

## 📱 Deployment

### Development
1. Connect iPhone via USB
2. Select device in Xcode
3. Click Run (⌘R)

### TestFlight (Beta Testing)
1. Archive the app in Xcode
2. Upload to App Store Connect
3. Add testers
4. Distribute via TestFlight

### App Store
1. Complete App Store Connect listing
2. Submit for review
3. Wait for approval

---

## 🎨 Design Implementation

Use your HTML mockup (`ios-mockup.html`) as a reference for:
- Color scheme
- Typography
- Spacing
- Component styles
- Layout structure

---

## 📚 Resources

- [SwiftUI Documentation](https://developer.apple.com/documentation/swiftui/)
- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [Swift Language Guide](https://docs.swift.org/swift-book/)

---

## 🚀 Quick Start Commands

```bash
# 1. Open Xcode
open -a Xcode

# 2. Create new project (via Xcode UI)

# 3. Start backend API
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# 4. Update Constants.swift with your API URL
# 5. Build and run in Xcode (⌘R)
```

---

## ✅ Next Steps

1. **Set up Xcode project** (30 min)
2. **Create Models** (1 hour)
3. **Build API Service** (2 hours)
4. **Create ViewModels** (2 hours)
5. **Build Views** (1-2 days)
6. **Test & Polish** (1 day)
7. **Deploy to TestFlight** (1 day)

**Total Estimated Time: 5-7 days**

---

Good luck with your iOS app development! 🎉


