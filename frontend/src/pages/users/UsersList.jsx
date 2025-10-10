import { useEffect, useState } from 'react';
import { getUsers } from '../../api/users';

export default function UsersList() {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        getUsers().then(res => setUsers(res.data)).finally(() => setLoading(false));
    }, []);

    if (loading) return <p>Cargando...</p>;

    return (
        <div>
            <h1 className="text-2xl mb-4">Usuarios</h1>
            <table className="table-auto w-full border">
                <thead className="bg-gray-200">
                    <tr>
                        <th className="border px-2 py-1">ID</th>
                        <th className="border px-2 py-1">Nombre</th>
                        <th className="border px-2 py-1">Email</th>
                        <th className="border px-2 py-1">Rol</th>
                    </tr>
                </thead>
                <tbody>
                    {users.map(u => (
                        <tr key={u.id}>
                            <td className="border px-2 py-1">{u.id}</td>
                            <td className="border px-2 py-1">{u.name}</td>
                            <td className="border px-2 py-1">{u.email}</td>
                            <td className="border px-2 py-1">{u.role}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
