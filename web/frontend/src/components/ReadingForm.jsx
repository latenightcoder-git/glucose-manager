import React, { useState } from 'react';
import { api } from '../api';
import { Button, TextField } from '@mui/material';

export default function ReadingForm({ patientId, onSaved }) {
  const [glucose, setGlucose] = useState(180);
  const [insulin, setInsulin] = useState(0);
  const [carbs, setCarbs] = useState(0);
  const [activity, setActivity] = useState(0.0);

  const save = async () => {
    await api.post('/api/readings', { patient_id: patientId, glucose, insulin, carbs, activity });
    onSaved && onSaved();
  };

  return (
    <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap: 8 }}>
      <TextField label="Glucose mg/dL" type="number" value={glucose} onChange={e=>setGlucose(+e.target.value)} />
      <TextField label="Insulin (U)" type="number" value={insulin} onChange={e=>setInsulin(+e.target.value)} />
      <TextField label="Carbs (g)" type="number" value={carbs} onChange={e=>setCarbs(+e.target.value)} />
      <TextField label="Activity (0-1)" type="number" value={activity} onChange={e=>setActivity(+e.target.value)} />
      <Button variant="contained" onClick={save} style={{ gridColumn:'1 / span 2' }}>Save Reading</Button>
    </div>
  );
}
