import React from 'react';
import { useForm } from 'react-hook-form';
import PublicLayout from '@/layout/PublicLayout';
import { createUser } from '@/api/users';
import { useNavigate } from 'react-router-dom';

export default function Register() {
    const navigate = useNavigate();
    const { register, handleSubmit } = useForm();

    const onSubmit = async (data) => {
        try {
            await createUser(data);
            alert('Usuario registrado correctamente');
            navigate('/login');
        } catch (err) {
            alert('Error al registrar usuario');
        }
    };

    return (
        <PublicLayout>
            <form
                onSubmit={handleSubmit(onSubmit)}
                className="p-6 border rounded shadow-md w-96 bg-white"
            >
                <h2 className="text-2xl mb-4 text-center font-bold">Registrar Usuario</h2>
                <input
                    {...register('name')}
                    placeholder="Nombre"
                    className="w-full mb-2 border px-2 py-1 rounded"
                />
                <input
                    {...register('email')}
                    type="email"
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
                    className="w-full bg-green-500 text-white py-2 rounded hover:bg-green-600"
                >
                    Registrar
                </button>
            </form>
        </PublicLayout>
    );
}
