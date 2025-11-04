import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { api } from '../api/client';

interface Recommendation {
  medication: string;
  priority: number;
  reasoning: string;
}

interface ScreeningResult {
  is_eligible: boolean;
  eligibility_message: string;
  bmi_category: string;
  recommended_drugs: Recommendation[];
  warnings: string[];
  screening_logic: Array<{ step: string; result: string }>;
}

const ScreeningResults: React.FC = () => {
  const { questionnaireId } = useParams<{ questionnaireId: string }>();
  const navigate = useNavigate();
  const [results, setResults] = useState<ScreeningResult | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchResults = async () => {
      try {
        const response = await api.getScreeningResults(parseInt(questionnaireId!));
        setResults(response.data);
      } catch (err: any) {
        setError('Failed to load screening results. Please try again.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchResults();
  }, [questionnaireId]);

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <h2>Loading your results...</h2>
      </div>
    );
  }

  if (error || !results) {
    return (
      <div style={{ maxWidth: '800px', margin: '50px auto', padding: '20px' }}>
        <div style={{
          backgroundColor: '#ffebee',
          color: '#c62828',
          padding: '20px',
          borderRadius: '4px'
        }}>
          {error || 'Results not found'}
        </div>
        <button
          onClick={() => navigate('/dashboard')}
          style={{
            marginTop: '20px',
            padding: '10px 20px',
            backgroundColor: '#1976d2',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Back to Dashboard
        </button>
      </div>
    );
  }

  return (
    <div style={{ maxWidth: '900px', margin: '20px auto', padding: '20px' }}>
      <h1>Your Screening Results</h1>

      {/* Eligibility Status */}
      <section style={{
        marginBottom: '30px',
        padding: '20px',
        backgroundColor: results.is_eligible ? '#e8f5e9' : '#ffebee',
        border: `2px solid ${results.is_eligible ? '#4caf50' : '#f44336'}`,
        borderRadius: '8px'
      }}>
        <h2 style={{ color: results.is_eligible ? '#2e7d32' : '#c62828', marginTop: 0 }}>
          {results.is_eligible ? '✓ You are eligible for oral AOMs' : '✗ Not Eligible'}
        </h2>
        <p style={{ fontSize: '16px' }}>{results.eligibility_message}</p>
        <p style={{ fontSize: '16px', marginTop: '10px' }}>
          <strong>BMI Category:</strong> {results.bmi_category}
        </p>
      </section>

      {/* Warnings */}
      {results.warnings && results.warnings.length > 0 && (
        <section style={{
          marginBottom: '30px',
          padding: '20px',
          backgroundColor: '#fff3e0',
          border: '2px solid #ff9800',
          borderRadius: '8px'
        }}>
          <h2 style={{ color: '#e65100', marginTop: 0 }}>Important Warnings</h2>
          <ul style={{ margin: 0 }}>
            {results.warnings.map((warning, index) => (
              <li key={index} style={{ marginBottom: '10px', fontSize: '16px' }}>
                {warning}
              </li>
            ))}
          </ul>
        </section>
      )}

      {/* Medication Recommendations */}
      {results.is_eligible && results.recommended_drugs.length > 0 && (
        <section style={{ marginBottom: '30px' }}>
          <h2>Recommended Medications</h2>
          <p style={{ color: '#666', marginBottom: '20px' }}>
            Based on your screening, the following medications are retained:
          </p>

          <div style={{
            padding: '20px',
            border: '2px solid #1976d2',
            borderRadius: '8px',
            backgroundColor: '#f9f9f9'
          }}>
            <ul style={{
              margin: 0,
              paddingLeft: '20px',
              fontSize: '18px',
              lineHeight: '2'
            }}>
              {results.recommended_drugs.map((drug, index) => (
                <li key={index}>{drug.medication}</li>
              ))}
            </ul>
          </div>
        </section>
      )}

      {/* Screening Process Details */}
      <section style={{
        marginBottom: '30px',
        padding: '20px',
        backgroundColor: '#f5f5f5',
        borderRadius: '8px'
      }}>
        <h2>How We Determined Your Results</h2>
        <ol style={{ marginTop: '15px' }}>
          {results.screening_logic.map((step, index) => (
            <li key={index} style={{ marginBottom: '15px' }}>
              <strong>{step.step}</strong>
              <br />
              <span style={{ color: '#666' }}>{step.result}</span>
            </li>
          ))}
        </ol>
      </section>

      {/* Next Steps */}
      <section style={{
        padding: '20px',
        backgroundColor: '#fff9c4',
        border: '2px solid #fbc02d',
        borderRadius: '8px',
        marginBottom: '30px'
      }}>
        <h2 style={{ marginTop: 0, color: '#f57f17' }}>Next Steps</h2>
        <ol style={{ marginBottom: 0 }}>
          <li style={{ marginBottom: '10px' }}>
            A doctor will review your questionnaire and these recommendations
          </li>
          <li style={{ marginBottom: '10px' }}>
            The doctor may contact you for additional questions or to schedule a consultation
          </li>
          <li style={{ marginBottom: '10px' }}>
            Final medication selection will be made by your doctor based on your complete medical history
          </li>
          <li>
            <strong>Do not</strong> start any medication without your doctor's approval
          </li>
        </ol>
      </section>

      <div style={{ display: 'flex', gap: '15px' }}>
        <button
          onClick={() => navigate('/dashboard')}
          style={{
            padding: '12px 24px',
            backgroundColor: '#1976d2',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            fontSize: '16px'
          }}
        >
          Back to Dashboard
        </button>
        <button
          onClick={() => window.print()}
          style={{
            padding: '12px 24px',
            backgroundColor: '#4caf50',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            fontSize: '16px'
          }}
        >
          Print Results
        </button>
      </div>
    </div>
  );
};

export default ScreeningResults;
