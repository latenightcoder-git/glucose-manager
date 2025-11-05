import React, { useEffect, useState } from 'react';
import { api } from '../api';
import { Button, Alert } from '@mui/material';
import { useAuth } from '../auth/AuthContext';

export default function PatientList({ onSelect }) {
  const [patients, setPatients] = useState([]);
  const [error, setError] = useState('');
  const { logout } = useAuth();
  const load = async () => {
    setError('');
    try {
      const res = await api.get('/api/patients');
      setPatients(res.data);
    } catch (err) {
      console.error('Failed loading patients', err);
      setPatients([]);
      const status = err.response?.status;
      if (status === 401) {
        setError('Not authorized. Please login again.');
      } else {
        setError(err.response?.data?.detail || err.message || 'Failed to load patients');
      }
    }
  };
  useEffect(()=>{ load(); },[]);
  return (
    <div>
      <h3>Patients</h3>
      {error && (
        <div style={{ marginBottom: 12 }}>
          <Alert severity="error">{error}</Alert>
          {error.includes('Not authorized') && (
            <div style={{ marginTop: 8 }}>
              <Button variant="outlined" onClick={() => { logout(); }}>Logout</Button>
            </div>
          )}
        </div>
      )}
      {patients.map(p => (
        <div key={p.id}>
          <Button onClick={()=>onSelect(p)}>{p.name} (#{p.id})</Button>
        </div>
      ))}
    </div>
  );
}
