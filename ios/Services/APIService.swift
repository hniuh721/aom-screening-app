import Foundation

class APIService {
    static let shared = APIService()
    // Use Mac IP address instead of localhost for iOS simulator
    // Change this to your Mac's IP address if different
    // To find your IP: run 'ifconfig | grep "inet " | grep -v 127.0.0.1' in terminal
    private let baseURL = "http://10.0.0.139:8000/api"
    
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
        
        let (responseData, response) = try await URLSession.shared.data(for: request)
        
        // Check HTTP status
        if let httpResponse = response as? HTTPURLResponse {
            if httpResponse.statusCode != 200 && httpResponse.statusCode != 201 {
                let errorMessage = String(data: responseData, encoding: .utf8) ?? "Unknown error"
                print("API Error (Status \(httpResponse.statusCode)): \(errorMessage)")
                throw NSError(domain: "APIService", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: "Server error: \(errorMessage)"])
            }
        }
        
        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        return try decoder.decode(Questionnaire.self, from: responseData)
    }
    
    func submitQuestionnaire(id: Int) async throws {
        guard let url = URL(string: "\(baseURL)/questionnaires/\(id)/submit") else {
            throw URLError(.badURL)
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        let (responseData, response) = try await URLSession.shared.data(for: request)
        
        // Check HTTP status
        if let httpResponse = response as? HTTPURLResponse {
            if httpResponse.statusCode != 200 && httpResponse.statusCode != 201 {
                let errorMessage = String(data: responseData, encoding: .utf8) ?? "Unknown error"
                print("API Error (Status \(httpResponse.statusCode)): \(errorMessage)")
                throw NSError(domain: "APIService", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: "Server error: \(errorMessage)"])
            }
        }
    }
    
    func runScreening(questionnaireId: Int) async throws -> ScreeningResult {
        guard let url = URL(string: "\(baseURL)/screening/run/\(questionnaireId)") else {
            throw URLError(.badURL)
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        // Check HTTP status
        if let httpResponse = response as? HTTPURLResponse {
            if httpResponse.statusCode != 200 && httpResponse.statusCode != 201 {
                let errorMessage = String(data: data, encoding: .utf8) ?? "Unknown error"
                print("API Error (Status \(httpResponse.statusCode)): \(errorMessage)")
                throw NSError(domain: "APIService", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: "Server error: \(errorMessage)"])
            }
        }
        
        // Print raw response for debugging
        if let responseString = String(data: data, encoding: .utf8) {
            print("API Response: \(responseString)")
        }
        
        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        
        do {
            return try decoder.decode(ScreeningResult.self, from: data)
        } catch {
            print("Decoding error: \(error)")
            if let responseString = String(data: data, encoding: .utf8) {
                print("Failed to decode response: \(responseString)")
            }
            throw error
        }
    }
    
    func getResults(questionnaireId: Int) async throws -> ScreeningResult {
        guard let url = URL(string: "\(baseURL)/screening/results/\(questionnaireId)") else {
            throw URLError(.badURL)
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "GET"
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        // Check HTTP status
        if let httpResponse = response as? HTTPURLResponse {
            if httpResponse.statusCode != 200 && httpResponse.statusCode != 201 {
                let errorMessage = String(data: data, encoding: .utf8) ?? "Unknown error"
                print("API Error (Status \(httpResponse.statusCode)): \(errorMessage)")
                throw NSError(domain: "APIService", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: "Server error: \(errorMessage)"])
            }
        }
        
        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        return try decoder.decode(ScreeningResult.self, from: data)
    }
}
