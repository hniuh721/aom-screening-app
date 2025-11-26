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
  age?: number;
  gender?: string;
  is_childbearing_age_woman?: boolean;
  bmi_category: string;
  recommended_drugs: Recommendation[];
  absolute_exclusions?: Record<string, string>;  // NEW: Hard eliminated drugs
  relative_warnings?: Record<string, string>;     // NEW: Caution/clearance required
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

      {/* NOT ELIGIBLE - BMI < 27 */}
      {!results.is_eligible && (
        <>
          {/* BMI Information */}
          <section style={{
            marginBottom: '30px',
            padding: '20px',
            backgroundColor: '#e3f2fd',
            border: '2px solid #1976d2',
            borderRadius: '8px'
          }}>
            <h2 style={{ color: '#1565c0', marginTop: 0 }}>
              Basic Information
            </h2>
            {results.age && (
              <p style={{ fontSize: '16px', marginTop: '10px', marginBottom: '5px' }}>
                <strong>Age:</strong> {results.age}{results.is_childbearing_age_woman && ' (childbearing age)'}
              </p>
            )}
            {results.gender && (
              <p style={{ fontSize: '16px', marginTop: '5px', marginBottom: '5px' }}>
                <strong>Gender:</strong> {results.gender.charAt(0).toUpperCase() + results.gender.slice(1)}
              </p>
            )}
            <p style={{ fontSize: '16px', marginTop: '5px' }}>
              <strong>BMI:</strong> {results.bmi_category}
            </p>
          </section>

          {/* Ineligibility Notice */}
          <section style={{
            marginBottom: '30px',
            padding: '30px',
            backgroundColor: '#ffebee',
            border: '3px solid #c62828',
            borderRadius: '8px'
          }}>
            <h2 style={{ color: '#c62828', marginTop: 0, fontSize: '24px' }}>
              ⛔ Not Eligible for Oral Anti-Obesity Medications
            </h2>
            <div style={{ fontSize: '16px', lineHeight: '1.8' }}>
              {results.warnings.map((warning, index) => (
                <p key={index} style={{ marginBottom: '10px' }}>
                  {warning}
                </p>
              ))}
            </div>
          </section>

          {/* Next Steps for Ineligible Patients */}
          <section style={{
            padding: '20px',
            backgroundColor: '#e8f5e9',
            border: '2px solid #4caf50',
            borderRadius: '8px',
            marginBottom: '30px'
          }}>
            <h2 style={{ marginTop: 0, color: '#2e7d32' }}>💡 Recommended Next Steps</h2>
            <ol style={{ marginBottom: 0, lineHeight: '1.8' }}>
              <li style={{ marginBottom: '10px' }}>
                <strong>Lifestyle Modifications:</strong> Focus on healthy eating patterns and regular physical activity
              </li>
              <li style={{ marginBottom: '10px' }}>
                <strong>Dietary Guidance:</strong> Consider working with a registered dietitian for personalized nutrition counseling
              </li>
              <li style={{ marginBottom: '10px' }}>
                <strong>Exercise Program:</strong> Aim for at least 150 minutes of moderate-intensity aerobic activity per week
              </li>
              <li style={{ marginBottom: '10px' }}>
                <strong>Medical Consultation:</strong> Discuss your weight management goals with your healthcare provider
              </li>
              <li>
                <strong>Reassessment:</strong> If your BMI changes in the future, you may become eligible for medication-assisted weight management
              </li>
            </ol>
          </section>
        </>
      )}

      {/* ELIGIBLE - BMI ≥ 27 - Show normal screening results */}
      {results.is_eligible && (
        <>
          {/* Screening Status */}
          <section style={{
            marginBottom: '30px',
            padding: '20px',
            backgroundColor: '#e3f2fd',
            border: '2px solid #1976d2',
            borderRadius: '8px'
          }}>
            <h2 style={{ color: '#1565c0', marginTop: 0 }}>
              Screening Completed
            </h2>
            {results.age && (
              <p style={{ fontSize: '16px', marginTop: '10px', marginBottom: '5px' }}>
                <strong>Age:</strong> {results.age}{results.is_childbearing_age_woman && ' (childbearing age)'}
              </p>
            )}
            {results.gender && (
              <p style={{ fontSize: '16px', marginTop: '5px', marginBottom: '5px' }}>
                <strong>Gender:</strong> {results.gender.charAt(0).toUpperCase() + results.gender.slice(1)}
              </p>
            )}
            <p style={{ fontSize: '16px', marginTop: '5px' }}>
              <strong>BMI:</strong> {results.bmi_category}
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
              <h2 style={{ color: '#e65100', marginTop: 0 }}>⚠️ Important Warnings</h2>
              <ul style={{ margin: 0 }}>
                {results.warnings.map((warning, index) => (
                  <li key={index} style={{ marginBottom: '10px', fontSize: '16px' }}>
                    {warning}
                  </li>
                ))}
              </ul>
            </section>
          )}

          {/* ABSOLUTE Exclusions */}
          {results.absolute_exclusions && Object.keys(results.absolute_exclusions).length > 0 && (
            <section style={{
              marginBottom: '30px',
              padding: '20px',
              backgroundColor: '#ffebee',
              border: '3px solid #c62828',
              borderRadius: '8px'
            }}>
              <h2 style={{ color: '#c62828', marginTop: 0 }}>⛔ ABSOLUTE Contraindications (Hard Eliminated)</h2>
              <p style={{ fontWeight: 'bold', marginBottom: '15px' }}>
                The following medications are completely excluded due to absolute contraindications:
              </p>
              <div style={{ backgroundColor: 'white', padding: '15px', borderRadius: '4px' }}>
                {Object.entries(results.absolute_exclusions).map(([drug, reason]) => (
                  <div key={drug} style={{
                    marginBottom: '15px',
                    paddingBottom: '15px',
                    borderBottom: '1px solid #ddd'
                  }}>
                    <div style={{ fontWeight: 'bold', fontSize: '16px', color: '#c62828', marginBottom: '5px' }}>
                      {drug}
                    </div>
                    <div style={{ fontSize: '14px', color: '#666' }}>
                      {reason}
                    </div>
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* RELATIVE Warnings */}
          {results.relative_warnings && Object.keys(results.relative_warnings).length > 0 && (
            <section style={{
              marginBottom: '30px',
              padding: '20px',
              backgroundColor: '#fffde7',
              border: '3px solid #f57f17',
              borderRadius: '8px'
            }}>
              <h2 style={{ color: '#f57f17', marginTop: 0 }}>⚠️ RELATIVE Contraindications (Caution/Clearance Required)</h2>
              <p style={{ fontWeight: 'bold', marginBottom: '15px' }}>
                The following medications may be considered BUT require special caution, specialist clearance, or enhanced monitoring:
              </p>
              <div style={{ backgroundColor: 'white', padding: '15px', borderRadius: '4px' }}>
                {Object.entries(results.relative_warnings).map(([drug, reason]) => (
                  <div key={drug} style={{
                    marginBottom: '15px',
                    paddingBottom: '15px',
                    borderBottom: '1px solid #ddd'
                  }}>
                    <div style={{ fontWeight: 'bold', fontSize: '16px', color: '#f57f17', marginBottom: '5px' }}>
                      {drug}
                    </div>
                    <div style={{ fontSize: '14px', color: '#666' }}>
                      {reason}
                    </div>
                  </div>
                ))}
              </div>
              <div style={{
                marginTop: '15px',
                padding: '10px',
                backgroundColor: '#fff9c4',
                borderLeft: '4px solid #f57f17',
                fontSize: '14px'
              }}>
                <strong>Important:</strong> Your doctor will assess whether these medications are appropriate for you based on your complete medical history and may require clearance from specialists (e.g., psychiatrist, cardiologist).
              </div>
            </section>
          )}

          {/* Medication Recommendations */}
          {results.recommended_drugs.length > 0 && (
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
        </>
      )}

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
