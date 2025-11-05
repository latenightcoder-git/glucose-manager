import React, { useState } from 'react';
import { api } from '../api';
import { Button, TextField, FormControlLabel, Checkbox } from '@mui/material';

export default function RecommendationPanel({ patientId }) {
  const [glucose, setGlucose] = useState(180);
  const [iob, setIob] = useState(1.0);
  const [carbs, setCarbs] = useState(0);
  const [activity, setActivity] = useState(0.0);
  const [exercising, setExercising] = useState(false);
  const [rec, setRec] = useState(null);

  const getRec = async () => {
    const res = await api.post('/api/recommend', {
      patient_id: patientId, glucose, insulin_on_board: iob, carbs, activity, exercising
    });
    setRec(res.data);
  };

  return (
    <div>
      <h3>Recommendation</h3>
      <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:8 }}>
        <TextField label="Glucose mg/dL" type="number" value={glucose} onChange={e=>setGlucose(+e.target.value)} />
        <TextField label="IOB (U)" type="number" value={iob} onChange={e=>setIob(+e.target.value)} />
        <TextField label="Carbs (g)" type="number" value={carbs} onChange={e=>setCarbs(+e.target.value)} />
        <TextField label="Activity (0-1)" type="number" value={activity} onChange={e=>setActivity(+e.target.value)} />
        <FormControlLabel control={<Checkbox checked={exercising} onChange={e=>setExercising(e.target.checked)} />} label="Exercising" />
      </div>
      <Button variant="outlined" onClick={getRec} style={{ marginTop: 8 }}>Get Recommendation</Button>
      {rec && <div style={{ marginTop: 8 }}>{rec.action_units.toFixed(2)}U — {rec.reason}</div>}
    </div>
  );
}
