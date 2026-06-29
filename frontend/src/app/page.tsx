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

export default function Home() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [isBackendConnected, setIsBackendConnected] = useState(false);

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
    <div className="flex h-screen w-screen bg-charcoal-950 overflow-hidden font-sans">
      {/* Sidebar Navigation */}
      <Sidebar 
        activeTab={activeTab} 
        setActiveTab={setActiveTab} 
        isBackendConnected={isBackendConnected} 
      />
      
      {/* Active Tab Viewport */}
      <main className="flex-1 flex flex-col min-w-0 h-screen relative overflow-hidden">
        {renderActiveView()}
      </main>
    </div>
  );
}
