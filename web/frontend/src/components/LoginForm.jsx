import React, { useState } from 'react';
import { Button, TextField, Alert } from '@mui/material';
import { useAuth } from '../auth/AuthContext';

export default function LoginForm() {
  const { login } = useAuth();
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('admin123');
  const [error, setError] = useState('');

  const onSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await login(username, password);
    } catch (err) {
      console.error('Login error:', err);
      setError(err.response?.data?.detail || err.message || 'Login failed');
    }
  };
  return (
    <form onSubmit={onSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 16, maxWidth: 300 }}>
      {error && <Alert severity="error">{error}</Alert>}
      <TextField label="Username" value={username} onChange={e=>setUsername(e.target.value)} fullWidth />
      <TextField label="Password" type="password" value={password} onChange={e=>setPassword(e.target.value)} fullWidth />
      <Button type="submit" variant="contained" fullWidth>Login</Button>
    </form>
  );
}
