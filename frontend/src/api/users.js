import axiosClient from '@/api/axiosClient';

export const getUsers = (params) => axiosClient.get('/users', { params });
export const getUser = (id) => axiosClient.get(`/users/${id}`);
export const createUser = (data) => axiosClient.post('/users', data);
export const updateUser = (id, data) => axiosClient.patch(`/users/${id}`, data);
export const deleteUser = (id) => axiosClient.delete(`/users/${id}`);
export const changePassword = (id, data) => axiosClient.post(`/users/${id}/password`, data);
