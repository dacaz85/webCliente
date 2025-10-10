import React from 'react';
import PublicHeader from '@/layout/PublicHeader';
import Footer from '@/layout/Footer';

export default function PublicLayout({ children }) {
    return (
        <div className="flex flex-col min-h-screen">
            <PublicHeader />
            <main className="flex-1 flex items-center justify-center p-4">
                {children}
            </main>
            <Footer />
        </div>
    );
}
