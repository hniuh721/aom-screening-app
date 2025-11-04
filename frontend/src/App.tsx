import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import PatientQuestionnaire from './pages/PatientQuestionnaire';
import ScreeningResults from './pages/ScreeningResults';

function App() {
  return (
    <Router>
      <div style={{ minHeight: '100vh', backgroundColor: '#f5f5f5' }}>
        <Routes>
          {/* Main questionnaire route */}
          <Route path="/questionnaire" element={<PatientQuestionnaire />} />

          {/* Results route */}
          <Route path="/results/:questionnaireId" element={<ScreeningResults />} />

          {/* Default redirect to questionnaire */}
          <Route path="/" element={<Navigate to="/questionnaire" replace />} />
          <Route path="*" element={<Navigate to="/questionnaire" replace />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App
