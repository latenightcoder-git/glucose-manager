import React from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, LineElement, CategoryScale, LinearScale, PointElement, Tooltip, Legend } from 'chart.js';
ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement, Tooltip, Legend);

export default function GlucoseChart({ readings }) {
  const labels = readings.map(r => r.ts);
  const data = {
    labels,
    datasets: [
      { label: 'Glucose', data: readings.map(r => r.glucose), borderColor: '#1976d2', tension: 0.1 }
    ]
  };
  const options = {
    plugins: {
      legend: { display: true }
    },
    scales: {
      y: { min: 40, max: 300 }
    }
  };
  return <Line data={data} options={options} />;
}
