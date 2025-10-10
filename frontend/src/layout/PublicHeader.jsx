// src/layout/PublicHeader.jsx
import React from 'react';

export default function PublicHeader() {
    return (
        <header className="h-16 flex items-center justify-between p-4 shadow-md font-sans bg-[#dc8502] z-10">
            <div className="text-4xl font-audiowide text-[#022CDC]">dacazMD</div>
            <div className="text-2xl font-bold text-black text-center flex-1">
                Portal Clientes
            </div>
        </header>
    );
}
