// src/context/AuthContext.jsx
import { createContext, useState, useEffect } from 'react';
import { login, refreshToken } from '@/api/auth';
import { jwtDecode } from 'jwt-decode';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);

    useEffect(() => {
        const token = localStorage.getItem('access_token');
        if (token) setUser(jwtDecode(token));
    }, []);

    const signIn = async (credentials) => {
        const { data } = await login(credentials);
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('refresh_token', data.refresh_token);
        setUser(jwtDecode(data.access_token));
    };

    const signOut = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        setUser(null);
    };

    const refreshAuthToken = async () => {
        const token = localStorage.getItem('refresh_token');
        if (!token) return signOut();
        try {
            const { data } = await refreshToken(token);
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('refresh_token', data.refresh_token);
            setUser(jwtDecode(data.access_token));
        } catch (err) {
            signOut();
        }
    };

    return (
        <AuthContext.Provider value={{ user, signIn, signOut, refreshAuthToken }}>
            {children}
        </AuthContext.Provider>
    );
};
