import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Dashboard: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div style={{ maxWidth: '900px', margin: '20px auto', padding: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px' }}>
        <div>
          <h1>AOM Screening Dashboard</h1>
          <p style={{ color: '#666' }}>Welcome, {user?.full_name}!</p>
        </div>
        <button
          onClick={handleLogout}
          style={{
            padding: '10px 20px',
            backgroundColor: '#f44336',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Logout
        </button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '30px' }}>
        <div style={{
          padding: '30px',
          backgroundColor: '#e3f2fd',
          border: '2px solid #1976d2',
          borderRadius: '8px',
          cursor: 'pointer'
        }}
        onClick={() => navigate('/questionnaire')}
        >
          <h2 style={{ marginTop: 0, color: '#1976d2' }}>Start New Screening</h2>
          <p style={{ color: '#333' }}>
            Fill out the questionnaire to get medication recommendations
          </p>
        </div>

        <div style={{
          padding: '30px',
          backgroundColor: '#f3e5f5',
          border: '2px solid #9c27b0',
          borderRadius: '8px',
          opacity: 0.6
        }}>
          <h2 style={{ marginTop: 0, color: '#9c27b0' }}>My History</h2>
          <p style={{ color: '#333' }}>
            View your previous screenings and results (Coming soon)
          </p>
        </div>
      </div>

      <section style={{
        padding: '20px',
        backgroundColor: '#fff3e0',
        border: '1px solid #ff9800',
        borderRadius: '8px'
      }}>
        <h2 style={{ marginTop: 0, color: '#e65100' }}>About This Screening</h2>
        <p>
          This screening tool helps determine which oral anti-obesity medications (AOMs) may be appropriate for you based on:
        </p>
        <ul>
          <li>Your BMI and weight-related health conditions</li>
          <li>Your medical history and current medications</li>
          <li>Your specific obesity-related symptoms</li>
          <li>Medical contraindications and safety considerations</li>
        </ul>
        <p>
          <strong>Important:</strong> This is a screening tool only. Final medication decisions must be made by your healthcare provider.
        </p>
      </section>
    </div>
  );
};

export default Dashboard;
