import SwiftUI

struct ContentView: View {
    @State private var age = ""
    @State private var gender = "male"
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
                    // Instructions Alert
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Instructions")
                            .font(.headline)
                        Text("All questions must be answered truthfully. False information may lead to incorrect medication selection and increased health risks.")
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                    }
                    .padding()
                    .background(Color.blue.opacity(0.1))
                    .cornerRadius(10)
                    .padding(.horizontal)
                    
                    // Section I: Basic Information
                    VStack(alignment: .leading, spacing: 12) {
                        Text("I. Basic Information")
                            .font(.title2)
                            .fontWeight(.bold)
                            .padding(.horizontal)
                        
                        Group {
                            TextField("Age *", text: $age)
                                .keyboardType(.numberPad)
                            
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
                            ("excessive_appetite", "Often feel very hungry and hard to control how much I eat"),
                            ("lack_of_satiety", "Don't feel full after eating, and get hungry again soon"),
                            ("binge_eating", "Sometimes eat a lot of food quickly and can't stop myself"),
                            ("emotional_eating", "Eat more when I'm anxious, sad, stressed, or in other mood swings"),
                            ("night_eating", "Eat a lot within 2 hours before bed, or wake up to eat at night"),
                            ("frequent_snacking", "Often eat snacks between regular meals"),
                            ("none", "None of the above situations")
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
                        Text("III. Medical Conditions & Health Status")
                            .font(.title2)
                            .fontWeight(.bold)
                            .padding(.horizontal)
                        
                        let conditions = [
                            ("hypertension", "Hypertension"),
                            ("dyslipidemia", "Dyslipidemia"),
                            ("coronary_artery_disease", "Coronary Artery Disease (CAD)"),
                            ("diabetes", "Type 2 Diabetes Mellitus (DM2)"),
                            ("sleep_apnea", "Obstructive Sleep Apnea (OSA)"),
                            ("arthritis", "Symptomatic arthritis of lower extremities"),
                            ("gerd", "Gastroesophageal Reflux Disease (GERD)"),
                            ("recurrent_kidney_stones", "Recurrent kidney stones"),
                            ("glaucoma", "Glaucoma"),
                            ("history_stroke", "Stroke"),
                            ("heart_disease", "Cardiovascular disease"),
                            ("adhd", "ADD/ADHD"),
                            ("psychiatric_treatment", "Psychiatric disorders"),
                            ("pregnancy_breastfeeding", "Currently pregnant"),
                            ("planning_pregnancy", "Planning to become pregnant within 3 months"),
                            ("none", "No above underlying medical conditions")
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
                        Text("IV. Medication and Allergy History")
                            .font(.title2)
                            .fontWeight(.bold)
                            .padding(.horizontal)
                        
                        TextField("Current Medications (prescription, OTC, supplements)", text: $currentMedications, axis: .vertical)
                            .textFieldStyle(.roundedBorder)
                            .lineLimit(3...6)
                            .padding(.horizontal)
                        
                        Toggle("Do you have any drug allergies?", isOn: $hasDrugAllergies)
                            .padding(.horizontal)
                        
                        if hasDrugAllergies {
                            TextField("List allergic drugs and reactions", text: $drugAllergies, axis: .vertical)
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
                        
                        TextField("Additional health conditions, lifestyle factors, or concerns", text: $additionalRemarks, axis: .vertical)
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
                    contactNumber: nil,
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
                guard let id = created.id else {
                    await MainActor.run {
                        errorMessage = "Failed to create questionnaire"
                        isLoading = false
                    }
                    return
                }
                
                try await APIService.shared.submitQuestionnaire(id: id)
                let result = try await APIService.shared.runScreening(questionnaireId: id)
                
                await MainActor.run {
                    screeningResult = result
                    showResults = true
                    isLoading = false
                }
            } catch {
                await MainActor.run {
                    // Show more detailed error message
                    if let nsError = error as NSError? {
                        if let detail = nsError.userInfo[NSLocalizedDescriptionKey] as? String {
                            errorMessage = detail
                        } else {
                            errorMessage = "Error: \(nsError.localizedDescription) (Code: \(nsError.code))"
                        }
                    } else {
                        errorMessage = "Error: \(error.localizedDescription)"
                    }
                    print("Full error: \(error)")
                    isLoading = false
                }
            }
        }
    }
}
