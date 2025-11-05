import React from 'react';
import { useAuth } from './AuthContext';

export default function ProtectedRoute({ allow, children }) {
    const { user } = useAuth();
    if (!user) return <div>Please login</div>;
    if (allow && !allow.includes(user.role)) return <div>Not authorized</div>;
    return children;
}
