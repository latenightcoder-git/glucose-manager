import React, { createContext, useContext, useState, useEffect } from 'react';
import { api, setAuth } from '../api';

const AuthCtx = createContext(null);
export function AuthProvider({ children }) {
    // Try to restore user from localStorage so refresh keeps login during dev
    const [user, setUser] = useState(() => {
        try {
            const raw = localStorage.getItem('glucose_user');
            return raw ? JSON.parse(raw) : null;
        } catch (e) { return null; }
    });
    // if we have a persisted user, ensure axios has the auth header set
    useEffect(()=>{
        if (user?.token) setAuth(user.token);
    }, [user]);
    const login = async (username, password) => {
    const res = await api.post('/api/login', { username, password });
    setAuth(res.data.token);
    const u = { username: res.data.username || username, role: res.data.role, token: res.data.token };
    setUser(u);
    try { localStorage.setItem('glucose_user', JSON.stringify(u)); } catch(e){}
    return res.data;
    };
    const logout = () => { setUser(null); setAuth(undefined); };
    return <AuthCtx.Provider value={{ user, login, logout }}>{children}</AuthCtx.Provider>;
}
export function useAuth() { return useContext(AuthCtx); }
