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
                        
                        Text(result.eligibilityMessage ?? "Screening completed successfully")
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
                        if let bmi = result.bmiCategory {
                            InfoRow(label: "BMI", value: bmi)
                        }
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
                        Text("1. A doctor will review your questionnaire and these recommendations")
                        Text("2. The doctor may contact you for additional questions or to schedule a consultation")
                        Text("3. Final medication selection will be made by your doctor based on your complete medical history")
                        Text("4. Do not start any medication without your doctor's approval")
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
