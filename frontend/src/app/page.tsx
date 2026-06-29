'use client';

import React, { useEffect, useState } from 'react';
import Sidebar from '../components/Sidebar';
import DashboardView from '../components/DashboardView';
import PredictionsView from '../components/PredictionsView';
import ChatbotView from '../components/ChatbotView';
import MenusView from '../components/MenusView';
import ReportsView from '../components/ReportsView';
import SettingsView from '../components/SettingsView';
import { pingBackend } from '../lib/api';
import { Menu, Zap } from 'lucide-react';

export default function Home() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [isBackendConnected, setIsBackendConnected] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  useEffect(() => {
    async function checkConnection() {
      const isAlive = await pingBackend();
      setIsBackendConnected(isAlive);
    }
    
    // Check initially
    checkConnection();
    
    // Check periodically every 15 seconds
    const interval = setInterval(checkConnection, 15000);
    return () => clearInterval(interval);
  }, []);

  const renderActiveView = () => {
    switch (activeTab) {
      case 'dashboard':
        return <DashboardView />;
      case 'predictions':
        return <PredictionsView />;
      case 'chatbot':
        return <ChatbotView />;
      case 'menus':
        return <MenusView />;
      case 'reports':
        return <ReportsView />;
      case 'settings':
        return <SettingsView />;
      default:
        return <DashboardView />;
    }
  };

  return (
    <div className="flex h-screen w-screen bg-charcoal-950 overflow-hidden font-sans relative">
      {/* Sidebar Navigation */}
      <Sidebar 
        activeTab={activeTab} 
        setActiveTab={setActiveTab} 
        isBackendConnected={isBackendConnected} 
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
      />
      
      {/* Active Tab Viewport */}
      <main className="flex-1 flex flex-col min-w-0 h-screen relative overflow-hidden">
        {/* Mobile Top Navbar */}
        <header className="md:hidden flex items-center justify-between px-6 py-4 bg-charcoal-900 border-b border-charcoal-800 shrink-0">
          <div className="flex items-center gap-3">
            <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-gold-400 to-gold-600 flex items-center justify-center">
              <Zap className="h-4.5 w-4.5 text-charcoal-950 stroke-[2.5]" />
            </div>
            <h1 className="font-extrabold text-md tracking-wider text-white">REAL.<span className="text-gold-500">i</span></h1>
          </div>
          
          <button 
            onClick={() => setIsSidebarOpen(true)}
            className="h-8 w-8 rounded-lg bg-charcoal-800 border border-charcoal-700 text-gold-400 font-bold hover:text-white flex items-center justify-center cursor-pointer"
            title="Expand Menu"
          >
            &lt;
          </button>
        </header>

        <div className="flex-1 overflow-hidden flex flex-col">
          {renderActiveView()}
        </div>
      </main>
    </div>
  );
}
