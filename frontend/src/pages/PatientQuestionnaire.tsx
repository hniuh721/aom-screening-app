import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api/client';

const PatientQuestionnaire: React.FC = () => {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  // Form state - all 7 sections
  const [formData, setFormData] = useState({
    // Section I: Basic Information
    name: '',
    age: '',
    gender: '',
    contact_number: '',
    is_childbearing_age_woman: false,

    // Section II: Eligibility
    has_medical_evaluation: false,
    attempted_lifestyle_modifications: false,
    has_reliable_contraception: false,
    bariatric_surgery_status: 'not_applicable',

    // Section III: BMI
    height_ft: '',
    height_in: '',
    weight_lb: '',
    comorbidities: [] as string[],

    // Section IV: Symptoms
    symptoms: [] as string[],

    // Section V: Health Conditions
    health_conditions: [] as string[],

    // Section VI: Medications
    current_medications: [] as string[],
    current_medications_text: '',
    has_drug_allergies: false,
    drug_allergies: [] as string[],
    drug_allergies_text: '',

    // Section VII: Additional Remarks
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
        contact_number: formData.contact_number || null,
        is_childbearing_age_woman: formData.is_childbearing_age_woman,
        has_medical_evaluation: formData.has_medical_evaluation,
        attempted_lifestyle_modifications: formData.attempted_lifestyle_modifications,
        has_reliable_contraception: formData.has_reliable_contraception,
        bariatric_surgery_status: formData.bariatric_surgery_status,
        height_ft: parseInt(formData.height_ft),
        height_in: parseInt(formData.height_in),
        weight_lb: parseFloat(formData.weight_lb),
        comorbidities: formData.comorbidities,
        symptoms: formData.symptoms,
        health_conditions: formData.health_conditions,
        current_medications: formData.current_medications,
        has_drug_allergies: formData.has_drug_allergies,
        drug_allergies: formData.drug_allergies,
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
        <ol style={{ marginBottom: 0, paddingLeft: '20px' }}>
          <li style={{ marginBottom: '10px' }}>
            <strong>All questions must be answered truthfully.</strong> False information may lead to incorrect medication selection and increased health risks.
          </li>
          <li style={{ marginBottom: 0 }}>
            After completion, please submit this questionnaire to your doctor. The doctor will determine the final applicable medication based on the questionnaire results and clinical evaluation.
          </li>
        </ol>
      </section>

      <form onSubmit={handleSubmit}>
        {/* Section I: Basic Information */}
        <section style={{ marginBottom: '30px', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
          <h2>I. Basic Information</h2>

          <div style={{ marginBottom: '15px' }}>
            <label>1. Name</label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              style={{ width: '100%', padding: '8px', marginTop: '5px' }}
            />
          </div>

          <div style={{ marginBottom: '15px' }}>
            <label>2. Age *</label>
            <input
              type="number"
              value={formData.age}
              onChange={(e) => setFormData({ ...formData, age: e.target.value })}
              required
              style={{ width: '100%', padding: '8px', marginTop: '5px' }}
              placeholder="years"
            />
          </div>

          <div style={{ marginBottom: '15px' }}>
            <label>3. Gender *</label>
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
            <label>4. Contact Number</label>
            <input
              type="tel"
              value={formData.contact_number}
              onChange={(e) => setFormData({ ...formData, contact_number: e.target.value })}
              style={{ width: '100%', padding: '8px', marginTop: '5px' }}
            />
          </div>

          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '8px' }}>
              5. Are you a woman of childbearing age (18-49 years old)?
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
        </section>

        {/* Section II: Eligibility Assessment */}
        <section style={{ marginBottom: '30px', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
          <h2>II. Eligibility Assessment for Oral AOMs</h2>
          <p style={{ fontStyle: 'italic', marginBottom: '20px' }}>(Please check "Yes" or "No" truthfully)</p>

          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold' }}>
              1. Have you completed a medical evaluation for obesity (including tests for TSH, fasting glucose, A1c, liver function, lipid panel) by a doctor, and have treatable causes of obesity (e.g., medication side effects, other diseases) been excluded (or you have not lost weight despite treatment for these causes)?
            </label>
            <div style={{ display: 'flex', gap: '20px' }}>
              <label>
                <input
                  type="radio"
                  name="medical_evaluation"
                  checked={formData.has_medical_evaluation === true}
                  onChange={() => setFormData({ ...formData, has_medical_evaluation: true })}
                  required
                />
                {' '}Yes
              </label>
              <label>
                <input
                  type="radio"
                  name="medical_evaluation"
                  checked={formData.has_medical_evaluation === false}
                  onChange={() => setFormData({ ...formData, has_medical_evaluation: false })}
                />
                {' '}No
              </label>
            </div>
          </div>

          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold' }}>
              2. Have you attempted lifestyle modifications (e.g., dietary control, regular physical activity) for at least 1 month, but achieved poor weight loss results (weight loss &lt; 3% of initial body weight), or have issues such as "excessive appetite, difficulty controlling cravings, binge eating, night eating"?
            </label>
            <div style={{ display: 'flex', gap: '20px' }}>
              <label>
                <input
                  type="radio"
                  name="lifestyle_modifications"
                  checked={formData.attempted_lifestyle_modifications === true}
                  onChange={() => setFormData({ ...formData, attempted_lifestyle_modifications: true })}
                  required
                />
                {' '}Yes
              </label>
              <label>
                <input
                  type="radio"
                  name="lifestyle_modifications"
                  checked={formData.attempted_lifestyle_modifications === false}
                  onChange={() => setFormData({ ...formData, attempted_lifestyle_modifications: false })}
                />
                {' '}No
              </label>
            </div>
          </div>

          {formData.is_childbearing_age_woman && (
            <div style={{ marginBottom: '20px' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold' }}>
                3. If you are a woman of childbearing age (18-49 years old), have you adopted reliable contraceptive methods (e.g., condoms, combined oral contraceptives, intrauterine devices)?
              </label>
              <div style={{ display: 'flex', gap: '20px' }}>
                <label>
                  <input
                    type="radio"
                    name="contraception"
                    checked={formData.has_reliable_contraception === true}
                    onChange={() => setFormData({ ...formData, has_reliable_contraception: true })}
                    required={formData.is_childbearing_age_woman}
                  />
                  {' '}Yes
                </label>
                <label>
                  <input
                    type="radio"
                    name="contraception"
                    checked={formData.has_reliable_contraception === false}
                    onChange={() => setFormData({ ...formData, has_reliable_contraception: false })}
                  />
                  {' '}No
                </label>
              </div>
              {formData.has_reliable_contraception === false && (
                <p style={{ color: '#d32f2f', fontSize: '14px', marginTop: '5px' }}>
                  (If "No" is selected, some medications may not be applicable)
                </p>
              )}
            </div>
          )}

          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold' }}>
              4. If you have undergone bariatric surgery, is it more than 6 months post-surgery, and have you experienced slow weight loss progress or an earlier-than-expected weight loss plateau while strictly following the dietary and exercise plan?
            </label>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              <label>
                <input
                  type="radio"
                  name="bariatric_surgery"
                  value="yes"
                  checked={formData.bariatric_surgery_status === 'yes'}
                  onChange={(e) => setFormData({ ...formData, bariatric_surgery_status: e.target.value })}
                  required
                />
                {' '}Yes
              </label>
              <label>
                <input
                  type="radio"
                  name="bariatric_surgery"
                  value="no"
                  checked={formData.bariatric_surgery_status === 'no'}
                  onChange={(e) => setFormData({ ...formData, bariatric_surgery_status: e.target.value })}
                />
                {' '}No
              </label>
              <label>
                <input
                  type="radio"
                  name="bariatric_surgery"
                  value="not_applicable"
                  checked={formData.bariatric_surgery_status === 'not_applicable'}
                  onChange={(e) => setFormData({ ...formData, bariatric_surgery_status: e.target.value })}
                />
                {' '}Have not undergone bariatric surgery
              </label>
            </div>
          </div>
        </section>

        {/* Section III: BMI Information */}
        <section style={{ marginBottom: '30px', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
          <h2>III. BMI-Related Information</h2>
          <p style={{ fontStyle: 'italic', fontSize: '14px', marginBottom: '20px' }}>
            (BMI = weight in kg / (height in m)²; used to determine medication priority)
          </p>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', marginBottom: '20px' }}>
            <div>
              <label>1. Height (feet) *</label>
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
            <label>2. Weight (lb) *</label>
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

          <div style={{ marginTop: '20px' }}>
            <label style={{ fontWeight: 'bold', display: 'block', marginBottom: '10px' }}>
              3. Do you have at least one of the following weight-related comorbidities? (multiple selections allowed)
            </label>
            <p style={{ fontSize: '13px', color: '#666', marginBottom: '10px' }}>
              Note: This question is particularly important if your BMI is 27-29.9
            </p>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '8px' }}>
              <label>
                <input
                  type="checkbox"
                  checked={formData.comorbidities.includes('hypertension')}
                  onChange={(e) => handleCheckboxChange('comorbidities', 'hypertension', e.target.checked)}
                />
                {' '}Hypertension
              </label>
              <label>
                <input
                  type="checkbox"
                  checked={formData.comorbidities.includes('dyslipidemia')}
                  onChange={(e) => handleCheckboxChange('comorbidities', 'dyslipidemia', e.target.checked)}
                />
                {' '}Dyslipidemia (HDL &lt; 50 mg/dL for women, HDL &lt; 40 mg/dL for men)
              </label>
              <label>
                <input
                  type="checkbox"
                  checked={formData.comorbidities.includes('coronary_artery_disease')}
                  onChange={(e) => handleCheckboxChange('comorbidities', 'coronary_artery_disease', e.target.checked)}
                />
                {' '}Coronary Artery Disease (CAD)
              </label>
              <label>
                <input
                  type="checkbox"
                  checked={formData.comorbidities.includes('diabetes')}
                  onChange={(e) => handleCheckboxChange('comorbidities', 'diabetes', e.target.checked)}
                />
                {' '}Type 2 Diabetes Mellitus (DM2)
              </label>
              <label>
                <input
                  type="checkbox"
                  checked={formData.comorbidities.includes('sleep_apnea')}
                  onChange={(e) => handleCheckboxChange('comorbidities', 'sleep_apnea', e.target.checked)}
                />
                {' '}Obstructive Sleep Apnea (OSA)
              </label>
              <label>
                <input
                  type="checkbox"
                  checked={formData.comorbidities.includes('arthritis')}
                  onChange={(e) => handleCheckboxChange('comorbidities', 'arthritis', e.target.checked)}
                />
                {' '}Symptomatic arthritis of lower extremities
              </label>
              <label>
                <input
                  type="checkbox"
                  checked={formData.comorbidities.includes('gerd')}
                  onChange={(e) => handleCheckboxChange('comorbidities', 'gerd', e.target.checked)}
                />
                {' '}Gastroesophageal Reflux Disease (GERD)
              </label>
              <label>
                <input
                  type="checkbox"
                  checked={formData.comorbidities.includes('none')}
                  onChange={(e) => handleCheckboxChange('comorbidities', 'none', e.target.checked)}
                />
                {' '}No above comorbidities (temporarily ineligible for oral AOMs)
              </label>
            </div>
          </div>
        </section>

        {/* Section IV: Symptoms */}
        <section style={{ marginBottom: '30px', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
          <h2>IV. Obesity-Related Symptoms</h2>
          <p style={{ fontStyle: 'italic', marginBottom: '15px' }}>(Please check all that apply to you)</p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <label>
              <input
                type="checkbox"
                checked={formData.symptoms.includes('excessive_appetite')}
                onChange={(e) => handleCheckboxChange('symptoms', 'excessive_appetite', e.target.checked)}
              />
              {' '}Excessive appetite, difficulty controlling food intake
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.symptoms.includes('lack_of_satiety')}
                onChange={(e) => handleCheckboxChange('symptoms', 'lack_of_satiety', e.target.checked)}
              />
              {' '}Lack of satiety, feeling hungry soon after eating
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.symptoms.includes('binge_eating')}
                onChange={(e) => handleCheckboxChange('symptoms', 'binge_eating', e.target.checked)}
              />
              {' '}Binge eating (consuming large amounts of food in a short time, unable to control voluntarily)
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.symptoms.includes('emotional_eating')}
                onChange={(e) => handleCheckboxChange('symptoms', 'emotional_eating', e.target.checked)}
              />
              {' '}Emotional eating (eating due to emotional fluctuations such as anxiety, depression, stress)
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.symptoms.includes('night_eating')}
                onChange={(e) => handleCheckboxChange('symptoms', 'night_eating', e.target.checked)}
              />
              {' '}Night eating (eating heavily within 2 hours before bedtime or waking up to eat at night)
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.symptoms.includes('frequent_snacking')}
                onChange={(e) => handleCheckboxChange('symptoms', 'frequent_snacking', e.target.checked)}
              />
              {' '}Frequent snacking (frequently eating snacks outside regular meal times)
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.symptoms.includes('no_symptoms')}
                onChange={(e) => handleCheckboxChange('symptoms', 'no_symptoms', e.target.checked)}
              />
              {' '}No obvious above symptoms
            </label>
          </div>
        </section>

        {/* Section V: Health Conditions */}
        <section style={{ marginBottom: '30px', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
          <h2>V. Underlying Medical Conditions & Health Status</h2>
          <p style={{ fontStyle: 'italic', marginBottom: '15px' }}>
            (Multiple selections allowed; please fill truthfully to avoid medication risks)
          </p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <label>
              <input
                type="checkbox"
                checked={formData.health_conditions.includes('uncontrolled_hypertension')}
                onChange={(e) => handleCheckboxChange('health_conditions', 'uncontrolled_hypertension', e.target.checked)}
              />
              {' '}Hypertension (uncontrolled: systolic blood pressure ≥ 140 mmHg or diastolic blood pressure ≥ 90 mmHg)
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.health_conditions.includes('controlled_hypertension')}
                onChange={(e) => handleCheckboxChange('health_conditions', 'controlled_hypertension', e.target.checked)}
              />
              {' '}Hypertension (controlled: systolic blood pressure &lt; 140 mmHg and diastolic blood pressure &lt; 90 mmHg)
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
                checked={formData.health_conditions.includes('adhd_on_medication')}
                onChange={(e) => handleCheckboxChange('health_conditions', 'adhd_on_medication', e.target.checked)}
              />
              {' '}ADD/ADHD (currently receiving medication treatment)
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.health_conditions.includes('psychiatric_treatment')}
                onChange={(e) => handleCheckboxChange('health_conditions', 'psychiatric_treatment', e.target.checked)}
              />
              {' '}Psychiatric disorders (e.g., anxiety disorder, bipolar disorder, depression; currently receiving treatment)
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

        {/* Section VI: Medications */}
        <section style={{ marginBottom: '30px', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
          <h2>VI. Medication and Allergy History</h2>

          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', marginBottom: '8px' }}>
              1. Please list all medications you are currently taking (including prescription drugs, over-the-counter drugs, and health supplements) along with their purposes:
            </label>
            <textarea
              value={formData.current_medications_text}
              onChange={(e) => setFormData({
                ...formData,
                current_medications_text: e.target.value,
                current_medications: e.target.value ? [e.target.value] : []
              })}
              placeholder="Example: Metformin 500mg - for diabetes control; Vitamin D 1000 IU - daily supplement"
              rows={3}
              style={{ width: '100%', padding: '8px', fontSize: '14px' }}
            />
          </div>

          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '8px' }}>
              2. Do you have any drug allergies?
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
                  onChange={() => setFormData({ ...formData, has_drug_allergies: false, drug_allergies_text: '', drug_allergies: [] })}
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
                  onChange={(e) => setFormData({
                    ...formData,
                    drug_allergies_text: e.target.value,
                    drug_allergies: e.target.value.split(',').map(s => s.trim()).filter(Boolean)
                  })}
                  placeholder="Example: Penicillin - rash and itching; Sulfa drugs - difficulty breathing"
                  rows={2}
                  style={{ width: '100%', padding: '8px', fontSize: '14px' }}
                />
              </div>
            )}
          </div>
        </section>

        {/* Section VII: Additional Remarks */}
        <section style={{ marginBottom: '30px', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
          <h2>VII. Additional Remarks</h2>
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
          {isLoading ? 'Submitting and Running Screening...' : 'Submit Questionnaire & Get Recommendations'}
        </button>
      </form>
    </div>
  );
};

export default PatientQuestionnaire;
