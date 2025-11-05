import React, { useEffect, useState } from 'react';
import { api } from '../api';
import ReadingForm from './ReadingForm';
import RecommendationPanel from './RecommendationPanel';
import GlucoseChart from './GlucoseChart';

export default function PatientDetails({ patient }) {
  const [readings, setReadings] = useState([]);
  const load = async () => {
    const res = await api.get(`/api/readings/${patient.id}`);
    setReadings(res.data);
  };
  useEffect(()=>{ load(); },[patient.id]);

  return (
    <div>
      <h2>{patient.name} (#{patient.id})</h2>
      <ReadingForm patientId={patient.id} onSaved={load} />
      <div style={{ marginTop: 16 }}>
        <RecommendationPanel patientId={patient.id} />
      </div>
      <div style={{ marginTop: 16 }}>
        <GlucoseChart readings={readings} />
      </div>
    </div>
  );
}
