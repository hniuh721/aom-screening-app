import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api/client';

const PatientQuestionnaire: React.FC = () => {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  // Form state - 5 sections
  const [formData, setFormData] = useState({
    // Section I: Basic Information
    age: '',
    gender: '',
    is_childbearing_age_woman: false,
    height_ft: '',
    height_in: '',
    weight_lb: '',

    // Section II: Eating Habits & Feelings
    eating_habits: [] as string[],

    // Section III: Medical Conditions & Health Status
    health_conditions: [] as string[],

    // Section IV: Medications
    current_medications_text: '',
    has_drug_allergies: false,
    drug_allergies_text: '',

    // Section V: Additional Remarks
    additional_remarks: ''
  });

  const handleCheckboxChange = (field: string, value: string, checked: boolean) => {
    setFormData(prev => ({
      ...prev,
      [field]: checked
        ? [...(prev[field as keyof typeof prev] as string[]), value]
        : (prev[field as keyof typeof prev] as string[]).filter(item => item !== value)
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      // Create questionnaire
      const questionnaireResponse = await api.createQuestionnaire({
        age: parseInt(formData.age),
        gender: formData.gender,
        is_childbearing_age_woman: formData.is_childbearing_age_woman,
        height_ft: parseInt(formData.height_ft),
        height_in: parseInt(formData.height_in),
        weight_lb: parseFloat(formData.weight_lb),
        eating_habits: formData.eating_habits,
        health_conditions: formData.health_conditions,
        current_medications: formData.current_medications_text ? [formData.current_medications_text] : [],
        has_drug_allergies: formData.has_drug_allergies,
        drug_allergies: formData.drug_allergies_text ? formData.drug_allergies_text.split(',').map(s => s.trim()).filter(Boolean) : [],
        additional_remarks: formData.additional_remarks || null
      });

      const questionnaireId = questionnaireResponse.data.id;

      // Submit questionnaire
      await api.submitQuestionnaire(questionnaireId);

      // Run screening
      await api.runScreening(questionnaireId);

      // Navigate to results
      navigate(`/results/${questionnaireId}`);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to submit questionnaire. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '800px', margin: '20px auto', padding: '20px' }}>
      <h1>Questionnaire for Screening Eligibility of Oral Anti-Obesity Medications (AOMs)</h1>

      {error && (
        <div style={{
          backgroundColor: '#ffebee',
          color: '#c62828',
          padding: '10px',
          borderRadius: '4px',
          marginBottom: '20px'
        }}>
          {error}
        </div>
      )}

      {/* Instructions */}
      <section style={{
        marginBottom: '30px',
        padding: '20px',
        backgroundColor: '#e3f2fd',
        border: '2px solid #1976d2',
        borderRadius: '8px'
      }}>
        <h3 style={{ marginTop: 0, color: '#1565c0' }}>Instructions for Completing the Questionnaire:</h3>
        <ul style={{ marginBottom: 0, paddingLeft: '20px' }}>
          <li style={{ marginBottom: '10px' }}>
            <strong>All questions must be answered truthfully.</strong> False information may lead to incorrect medication selection and increased health risks.
          </li>
          <li style={{ marginBottom: 0 }}>
            After completion, please submit this questionnaire to your doctor. The doctor will determine the final applicable medication based on the questionnaire results and clinical evaluation.
          </li>
        </ul>
      </section>

      <form onSubmit={handleSubmit}>
        {/* Section I: Basic Information */}
        <section style={{ marginBottom: '30px', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
          <h2>I. Basic Information</h2>

          <div style={{ marginBottom: '15px' }}>
            <label>Age *</label>
            <input
              type="number"
              value={formData.age}
              onChange={(e) => setFormData({ ...formData, age: e.target.value })}
              required
              style={{ width: '100%', padding: '8px', marginTop: '5px' }}
            />
          </div>

          <div style={{ marginBottom: '15px' }}>
            <label>Gender *</label>
            <div style={{ marginTop: '5px', display: 'flex', gap: '20px' }}>
              <label>
                <input
                  type="radio"
                  name="gender"
                  value="male"
                  checked={formData.gender === 'male'}
                  onChange={(e) => setFormData({ ...formData, gender: e.target.value })}
                  required
                />
                {' '}Male
              </label>
              <label>
                <input
                  type="radio"
                  name="gender"
                  value="female"
                  checked={formData.gender === 'female'}
                  onChange={(e) => setFormData({ ...formData, gender: e.target.value })}
                />
                {' '}Female
              </label>
              <label>
                <input
                  type="radio"
                  name="gender"
                  value="other"
                  checked={formData.gender === 'other'}
                  onChange={(e) => setFormData({ ...formData, gender: e.target.value })}
                />
                {' '}Other
              </label>
            </div>
          </div>

          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '8px' }}>
              Are you a woman of childbearing age (18-49 years old)?
            </label>
            <div style={{ display: 'flex', gap: '20px' }}>
              <label>
                <input
                  type="radio"
                  name="childbearing_age"
                  checked={formData.is_childbearing_age_woman === true}
                  onChange={() => setFormData({ ...formData, is_childbearing_age_woman: true })}
                />
                {' '}Yes
              </label>
              <label>
                <input
                  type="radio"
                  name="childbearing_age"
                  checked={formData.is_childbearing_age_woman === false}
                  onChange={() => setFormData({ ...formData, is_childbearing_age_woman: false })}
                />
                {' '}No
              </label>
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', marginBottom: '20px' }}>
            <div>
              <label>Height (feet) *</label>
              <input
                type="number"
                value={formData.height_ft}
                onChange={(e) => setFormData({ ...formData, height_ft: e.target.value })}
                required
                min="3"
                max="8"
                style={{ width: '100%', padding: '8px', marginTop: '5px' }}
                placeholder="ft"
              />
            </div>
            <div>
              <label>Height (inches) *</label>
              <input
                type="number"
                value={formData.height_in}
                onChange={(e) => setFormData({ ...formData, height_in: e.target.value })}
                required
                min="0"
                max="11"
                style={{ width: '100%', padding: '8px', marginTop: '5px' }}
                placeholder="in"
              />
            </div>
          </div>

          <div style={{ marginBottom: '20px' }}>
            <label>Weight (lb) *</label>
            <input
              type="number"
              step="0.1"
              value={formData.weight_lb}
              onChange={(e) => setFormData({ ...formData, weight_lb: e.target.value })}
              required
              style={{ width: '100%', padding: '8px', marginTop: '5px' }}
              placeholder="pounds"
            />
          </div>
          <p style={{ fontSize: '13px', color: '#666', fontStyle: 'italic' }}>
            (BMI value will be calculated and displayed in the final result)
          </p>
        </section>

        {/* Section II: Eating Habits & Feelings */}
        <section style={{ marginBottom: '30px', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
          <h2>II. Eating Habits & Feelings</h2>
          <p style={{ fontStyle: 'italic', marginBottom: '15px' }}>(Please check all that apply to you)</p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <label>
              <input
                type="checkbox"
                checked={formData.eating_habits.includes('excessive_appetite')}
                onChange={(e) => handleCheckboxChange('eating_habits', 'excessive_appetite', e.target.checked)}
              />
              {' '}Often feel very hungry and hard to control how much I eat
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.eating_habits.includes('lack_of_satiety')}
                onChange={(e) => handleCheckboxChange('eating_habits', 'lack_of_satiety', e.target.checked)}
              />
              {' '}Don't feel full after eating, and get hungry again soon
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.eating_habits.includes('binge_eating')}
                onChange={(e) => handleCheckboxChange('eating_habits', 'binge_eating', e.target.checked)}
              />
              {' '}Sometimes eat a lot of food quickly and can't stop myself
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.eating_habits.includes('emotional_eating')}
                onChange={(e) => handleCheckboxChange('eating_habits', 'emotional_eating', e.target.checked)}
              />
              {' '}Eat more when I'm anxious, sad, stressed, or in other mood swings
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.eating_habits.includes('night_eating')}
                onChange={(e) => handleCheckboxChange('eating_habits', 'night_eating', e.target.checked)}
              />
              {' '}Eat a lot within 2 hours before bed, or wake up to eat at night
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.eating_habits.includes('frequent_snacking')}
                onChange={(e) => handleCheckboxChange('eating_habits', 'frequent_snacking', e.target.checked)}
              />
              {' '}Often eat snacks between regular meals
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.eating_habits.includes('none')}
                onChange={(e) => handleCheckboxChange('eating_habits', 'none', e.target.checked)}
              />
              {' '}None of the above situations
            </label>
          </div>
        </section>

        {/* Section III: Medical Conditions & Health Status */}
        <section style={{ marginBottom: '30px', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
          <h2>III. Medical Conditions & Health Status</h2>
          <p style={{ fontStyle: 'italic', marginBottom: '15px' }}>
            (Multiple selections allowed; please fill truthfully to avoid medication risks)
          </p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <label>
              <input
                type="checkbox"
                checked={formData.health_conditions.includes('hypertension')}
                onChange={(e) => handleCheckboxChange('health_conditions', 'hypertension', e.target.checked)}
              />
              {' '}Hypertension
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.health_conditions.includes('dyslipidemia')}
                onChange={(e) => handleCheckboxChange('health_conditions', 'dyslipidemia', e.target.checked)}
              />
              {' '}Dyslipidemia (HDL &lt; 50 mg/dL for women, HDL &lt; 40 mg/dL for men)
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.health_conditions.includes('coronary_artery_disease')}
                onChange={(e) => handleCheckboxChange('health_conditions', 'coronary_artery_disease', e.target.checked)}
              />
              {' '}Coronary Artery Disease (CAD)
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.health_conditions.includes('diabetes')}
                onChange={(e) => handleCheckboxChange('health_conditions', 'diabetes', e.target.checked)}
              />
              {' '}Type 2 Diabetes Mellitus (DM2)
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.health_conditions.includes('sleep_apnea')}
                onChange={(e) => handleCheckboxChange('health_conditions', 'sleep_apnea', e.target.checked)}
              />
              {' '}Obstructive Sleep Apnea (OSA)
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.health_conditions.includes('arthritis')}
                onChange={(e) => handleCheckboxChange('health_conditions', 'arthritis', e.target.checked)}
              />
              {' '}Symptomatic arthritis of lower extremities
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.health_conditions.includes('gerd')}
                onChange={(e) => handleCheckboxChange('health_conditions', 'gerd', e.target.checked)}
              />
              {' '}Gastroesophageal Reflux Disease (GERD)
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.health_conditions.includes('no_comorbidities')}
                onChange={(e) => handleCheckboxChange('health_conditions', 'no_comorbidities', e.target.checked)}
              />
              {' '}No above comorbidities (temporarily ineligible for oral AOMs)
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.health_conditions.includes('recurrent_kidney_stones')}
                onChange={(e) => handleCheckboxChange('health_conditions', 'recurrent_kidney_stones', e.target.checked)}
              />
              {' '}Recurrent kidney stones
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.health_conditions.includes('glaucoma')}
                onChange={(e) => handleCheckboxChange('health_conditions', 'glaucoma', e.target.checked)}
              />
              {' '}Glaucoma
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.health_conditions.includes('history_stroke')}
                onChange={(e) => handleCheckboxChange('health_conditions', 'history_stroke', e.target.checked)}
              />
              {' '}Stroke
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.health_conditions.includes('heart_disease')}
                onChange={(e) => handleCheckboxChange('health_conditions', 'heart_disease', e.target.checked)}
              />
              {' '}Cardiovascular disease (e.g., coronary artery disease, heart failure)
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.health_conditions.includes('intracranial_hypertension')}
                onChange={(e) => handleCheckboxChange('health_conditions', 'intracranial_hypertension', e.target.checked)}
              />
              {' '}Intracranial hypertension
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.health_conditions.includes('adhd')}
                onChange={(e) => handleCheckboxChange('health_conditions', 'adhd', e.target.checked)}
              />
              {' '}ADD/ADHD
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.health_conditions.includes('psychiatric_treatment')}
                onChange={(e) => handleCheckboxChange('health_conditions', 'psychiatric_treatment', e.target.checked)}
              />
              {' '}Psychiatric disorders (e.g., anxiety disorder, bipolar disorder, depression)
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.health_conditions.includes('thyroid_cancer')}
                onChange={(e) => handleCheckboxChange('health_conditions', 'thyroid_cancer', e.target.checked)}
              />
              {' '}Medullary thyroid cancer
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.health_conditions.includes('history_pancreatitis')}
                onChange={(e) => handleCheckboxChange('health_conditions', 'history_pancreatitis', e.target.checked)}
              />
              {' '}Pancreatitis
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.health_conditions.includes('gastroparesis')}
                onChange={(e) => handleCheckboxChange('health_conditions', 'gastroparesis', e.target.checked)}
              />
              {' '}Gastroparesis
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.health_conditions.includes('taking_tamoxifen')}
                onChange={(e) => handleCheckboxChange('health_conditions', 'taking_tamoxifen', e.target.checked)}
              />
              {' '}Currently taking Tamoxifen (an anti-cancer medication)
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.health_conditions.includes('pregnancy_breastfeeding')}
                onChange={(e) => handleCheckboxChange('health_conditions', 'pregnancy_breastfeeding', e.target.checked)}
              />
              {' '}Currently pregnant
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.health_conditions.includes('planning_pregnancy')}
                onChange={(e) => handleCheckboxChange('health_conditions', 'planning_pregnancy', e.target.checked)}
              />
              {' '}Planning to become pregnant within 3 months
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.health_conditions.includes('history_drug_abuse')}
                onChange={(e) => handleCheckboxChange('health_conditions', 'history_drug_abuse', e.target.checked)}
              />
              {' '}History of substance abuse (e.g., amphetamine abuse)
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.health_conditions.includes('hyperthyroidism')}
                onChange={(e) => handleCheckboxChange('health_conditions', 'hyperthyroidism', e.target.checked)}
              />
              {' '}Thyroid dysfunction (hyperthyroidism/hypothyroidism)
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.health_conditions.includes('none')}
                onChange={(e) => handleCheckboxChange('health_conditions', 'none', e.target.checked)}
              />
              {' '}No above underlying medical conditions or health status
            </label>
          </div>
        </section>

        {/* Section IV: Medication and Allergy History */}
        <section style={{ marginBottom: '30px', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
          <h2>IV. Medication and Allergy History</h2>

          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', marginBottom: '8px' }}>
              Please list all medications you are currently taking (including prescription drugs, over-the-counter drugs, and health supplements) along with their purposes:
            </label>
            <textarea
              value={formData.current_medications_text}
              onChange={(e) => setFormData({ ...formData, current_medications_text: e.target.value })}
              placeholder="Example: Metformin 500mg - for diabetes control; Vitamin D 1000 IU - daily supplement"
              rows={3}
              style={{ width: '100%', padding: '8px', fontSize: '14px' }}
            />
          </div>

          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '8px' }}>
              Do you have any drug allergies?
            </label>
            <div style={{ display: 'flex', gap: '20px', marginBottom: '10px' }}>
              <label>
                <input
                  type="radio"
                  name="drug_allergies"
                  checked={formData.has_drug_allergies === true}
                  onChange={() => setFormData({ ...formData, has_drug_allergies: true })}
                />
                {' '}Yes
              </label>
              <label>
                <input
                  type="radio"
                  name="drug_allergies"
                  checked={formData.has_drug_allergies === false}
                  onChange={() => setFormData({ ...formData, has_drug_allergies: false, drug_allergies_text: '' })}
                />
                {' '}No
              </label>
            </div>

            {formData.has_drug_allergies && (
              <div style={{ marginTop: '10px' }}>
                <label style={{ display: 'block', marginBottom: '8px' }}>
                  If "Yes", please list the names of allergic drugs and the allergic reactions (e.g., rash, difficulty breathing):
                </label>
                <textarea
                  value={formData.drug_allergies_text}
                  onChange={(e) => setFormData({ ...formData, drug_allergies_text: e.target.value })}
                  placeholder="Example: Penicillin - rash and itching; Sulfa drugs - difficulty breathing"
                  rows={2}
                  style={{ width: '100%', padding: '8px', fontSize: '14px' }}
                />
              </div>
            )}
          </div>
        </section>

        {/* Section V: Additional Remarks */}
        <section style={{ marginBottom: '30px', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
          <h2>V. Additional Remarks</h2>
          <label style={{ display: 'block', marginBottom: '8px' }}>
            Do you have any unmentioned health conditions, living habits, or concerns that may affect the selection of oral anti-obesity medications?
          </label>
          <textarea
            value={formData.additional_remarks}
            onChange={(e) => setFormData({ ...formData, additional_remarks: e.target.value })}
            placeholder="Please describe any additional health conditions, lifestyle factors, or concerns..."
            rows={4}
            style={{ width: '100%', padding: '8px', fontSize: '14px' }}
          />
        </section>

        <button
          type="submit"
          disabled={isLoading}
          style={{
            width: '100%',
            padding: '15px',
            fontSize: '18px',
            backgroundColor: isLoading ? '#ccc' : '#1976d2',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: isLoading ? 'not-allowed' : 'pointer',
            fontWeight: 'bold'
          }}
        >
          {isLoading ? 'Submitting...' : 'Submit'}
        </button>
      </form>
    </div>
  );
};

export default PatientQuestionnaire;
