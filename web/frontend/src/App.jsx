import React from 'react';
import { AuthProvider, useAuth } from './auth/AuthContext';
import ProtectedRoute from './auth/ProtectedRoute';
import LoginForm from './components/LoginForm';
import Dashboard from './pages/Dashboard';
import { Button } from '@mui/material';

function Shell() {
  const { user, logout } = useAuth();
  return (
    <div style={{ padding: 16 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1 style={{ margin: 0 }}>Glucose Manager</h1>
        <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
          {user && <div style={{ fontSize: 14 }}>Signed in as <strong>{user.username}</strong> ({user.role})</div>}
          {user && <Button variant="outlined" onClick={() => logout()}>Logout</Button>}
        </div>
      </div>

      {!user ? <LoginForm /> :
        <ProtectedRoute allow={['admin', 'doctor', 'nurse', 'patient', 'family']}>
          <Dashboard />
        </ProtectedRoute>
      }
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <Shell />
    </AuthProvider>
  );
}
