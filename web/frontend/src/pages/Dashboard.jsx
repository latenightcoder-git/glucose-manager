import React, { useState } from 'react';
import PatientList from '../components/PatientList';
import PatientDetails from '../components/PatientDetails';

export default function Dashboard() {
  const [selected, setSelected] = useState(null);
  return (
    <div style={{ display: 'grid', gridTemplateColumns: '300px 1fr', gap: 16 }}>
      <div><PatientList onSelect={setSelected} /></div>
      <div>{selected ? <PatientDetails patient={selected} /> : <div>Select a patient</div>}</div>
    </div>
  );
}
