import axiosClient from '@/api/axiosClient';

// Login con JSON { email, password }
export const login = (data) => {
    return axiosClient.post('/auth/login', data, {
        headers: { 'Content-Type': 'application/json' }
    });
};

// Refresh token
export const refreshToken = (refresh_token) =>
    axiosClient.post('/auth/refresh', { refresh_token });

// Logout (opcional)
export const logout = () => axiosClient.post('/auth/logout');