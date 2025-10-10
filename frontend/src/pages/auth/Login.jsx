import React from 'react';
import { useForm } from 'react-hook-form';
import { useAuth } from '@/hooks/useAuth';
import { useNavigate } from 'react-router-dom';
import PublicLayout from '@/layout/PublicLayout';

export default function Login() {
    const { signIn } = useAuth();
    const navigate = useNavigate();
    const { register, handleSubmit } = useForm();

    const onSubmit = async (data) => {
        try {
            await signIn(data); // data = { email, password }
            navigate('/');       // redirige al dashboard
        } catch (err) {
            console.error(err.response?.data || err);
            alert('Credenciales inválidas');
        }
    };

    return (
        <PublicLayout>
            <form
                onSubmit={handleSubmit(onSubmit)}
                className="p-6 border rounded shadow-md w-96 bg-white"
            >
                <h2 className="text-2xl mb-4 text-center font-bold">Login</h2>
                <input
                    {...register('email')}
                    placeholder="Email"
                    className="w-full mb-2 border px-2 py-1 rounded"
                />
                <input
                    {...register('password')}
                    type="password"
                    placeholder="Contraseña"
                    className="w-full mb-4 border px-2 py-1 rounded"
                />
                <button
                    type="submit"
                    className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
                >
                    Iniciar sesión
                </button>
            </form>
        </PublicLayout>
    );
}
