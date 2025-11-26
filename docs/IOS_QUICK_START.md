# iOS App Quick Start Checklist

## ✅ Pre-Development Checklist

- [ ] Mac computer ready
- [ ] Xcode 15+ installed (from Mac App Store)
- [ ] Apple Developer Account created (free for development)
- [ ] Backend API running (`uvicorn app.main:app --reload`)
- [ ] Tested API endpoints in browser (http://localhost:8000/docs)

---

## 🚀 Day-by-Day Plan

### Day 1: Setup & Foundation (4-6 hours)

- [ ] Create new Xcode project
  - Product Name: `AOMScreening`
  - Interface: SwiftUI
  - Language: Swift
  
- [ ] Create folder structure:
  ```
  Models/
  Views/
  ViewModels/
  Services/
  Utilities/
  ```

- [ ] Create `Models/Questionnaire.swift`
- [ ] Create `Models/ScreeningResult.swift`
- [ ] Create `Utilities/Constants.swift`
- [ ] Test: Build project (⌘B) - should succeed

**Goal:** Project compiles without errors

---

### Day 2: API Integration (4-6 hours)

- [ ] Create `Services/NetworkManager.swift`
- [ ] Create `Services/APIService.swift`
- [ ] Test API connection:
  ```swift
  // Add test function in APIService
  func testConnection() async {
      // Try creating a simple questionnaire
  }
  ```
- [ ] Update `Constants.swift` with correct API URL
- [ ] Test: Run app, check console for API calls

**Goal:** App can communicate with backend API

---

### Day 3: ViewModels (3-4 hours)

- [ ] Create `ViewModels/QuestionnaireViewModel.swift`
- [ ] Create `ViewModels/ResultsViewModel.swift`
- [ ] Test: ViewModels compile and handle state

**Goal:** Business logic separated from UI

---

### Day 4: Basic UI (4-6 hours)

- [ ] Create `Views/Components/IOSCard.swift`
- [ ] Create `Views/Questionnaire/BasicInfoView.swift`
- [ ] Update main `QuestionnaireView.swift`
- [ ] Test: UI displays correctly

**Goal:** Basic form visible and functional

---

### Day 5: Complete Questionnaire (4-6 hours)

- [ ] Create `Views/Questionnaire/EatingHabitsView.swift`
- [ ] Create `Views/Questionnaire/MedicalConditionsView.swift`
- [ ] Create `Views/Questionnaire/MedicationsView.swift`
- [ ] Create `Views/Questionnaire/AdditionalRemarksView.swift`
- [ ] Test: All sections work, form can be filled

**Goal:** Complete questionnaire form functional

---

### Day 6: Results & Polish (4-6 hours)

- [ ] Create `Views/Results/ResultsView.swift`
- [ ] Add navigation between questionnaire and results
- [ ] Add loading states
- [ ] Add error handling
- [ ] Test: Full flow works end-to-end

**Goal:** Complete app flow works

---

### Day 7: Testing & Deployment Prep (3-4 hours)

- [ ] Test on iPhone simulator
- [ ] Test on physical device
- [ ] Fix any bugs
- [ ] Add app icon
- [ ] Prepare for TestFlight

**Goal:** App ready for beta testing

---

## 🔧 Essential Code Snippets

### 1. Info.plist Configuration (for localhost API)

Add to `Info.plist`:
```xml
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsLocalNetworking</key>
    <true/>
</dict>
```

### 2. Test API Connection

```swift
// In your view
Task {
    do {
        let result = try await APIService.shared.getScreeningResults(questionnaireId: 1)
        print("Success: \(result)")
    } catch {
        print("Error: \(error)")
    }
}
```

### 3. Preview Provider (for SwiftUI previews)

```swift
#Preview {
    QuestionnaireView()
}
```

---

## 🐛 Common Issues & Solutions

### Issue: "Cannot connect to localhost"
**Solution:** 
- Use your Mac's IP address instead: `http://192.168.1.X:8000`
- Or use `http://127.0.0.1:8000`
- Add NSAppTransportSecurity to Info.plist

### Issue: "Decoding error"
**Solution:**
- Check that model property names match API response
- Verify CodingKeys are correct
- Print raw JSON to debug

### Issue: "Build failed"
**Solution:**
- Clean build folder: Product → Clean Build Folder (⇧⌘K)
- Delete DerivedData
- Restart Xcode

---

## 📱 Testing Checklist

- [ ] App launches without crashing
- [ ] All form fields accept input
- [ ] Segmented controls work
- [ ] Switches toggle correctly
- [ ] Checkboxes can be selected
- [ ] Form validation works
- [ ] Submit button triggers API call
- [ ] Loading state shows during submission
- [ ] Results page displays correctly
- [ ] Error messages show when API fails
- [ ] Navigation works (back buttons, etc.)

---

## 🎯 Success Criteria

Your app is ready when:
- ✅ All 5 questionnaire sections are complete
- ✅ Form data is sent to API correctly
- ✅ Results page displays screening results
- ✅ App works on iPhone simulator
- ✅ No crashes or major bugs
- ✅ UI matches your HTML mockup design

---

## 📞 Need Help?

1. Check the full guide: `IOS_APP_GUIDE.md`
2. Review your HTML mockup: `ios-mockup.html`
3. Test API endpoints: http://localhost:8000/docs
4. SwiftUI documentation: https://developer.apple.com/documentation/swiftui/

---

**You've got this! Start with Day 1 and work through step by step.** 🚀


