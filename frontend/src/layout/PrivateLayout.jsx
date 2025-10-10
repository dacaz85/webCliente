import Sidebar from './Sidebar';
import Header from './Header';
import Footer from './Footer';
import { useAuth } from '../hooks/useAuth';
import { Navigate, Outlet } from 'react-router-dom';

export default function PrivateLayout() {
    const { user } = useAuth();
    if (!user) return <Navigate to="/login" />;

    return (
        <div className="flex h-screen">
            <Sidebar />
            <div className="flex-1 flex flex-col">
                <Header />
                <main className="flex-1 p-4 overflow-auto">
                    <Outlet />
                </main>
                <Footer />
            </div>
        </div>
    );
}
