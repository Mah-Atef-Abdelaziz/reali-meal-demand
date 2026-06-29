import React, { useState } from 'react';
import { 
  LayoutDashboard, 
  TrendingUp, 
  MessageSquare, 
  FileText, 
  MenuSquare, 
  Settings, 
  Zap
} from 'lucide-react';

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  isBackendConnected: boolean;
  isOpen: boolean;
  onClose: () => void;
}

export default function Sidebar({ activeTab, setActiveTab, isBackendConnected, isOpen, onClose }: SidebarProps) {
  const [isDesktopCollapsed, setIsDesktopCollapsed] = useState(false);

  const menuItems = [
    { id: 'dashboard', name: 'Dashboard', icon: LayoutDashboard },
    { id: 'predictions', name: 'Predictions', icon: TrendingUp },
    { id: 'chatbot', name: 'Smart Assistant', icon: MessageSquare },
    { id: 'menus', name: 'Menu Planning', icon: MenuSquare },
    { id: 'reports', name: 'Reports & Logs', icon: FileText },
    { id: 'settings', name: 'System Settings', icon: Settings },
  ];

  return (
    <>
      {/* Mobile Overlay Background */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 md:hidden"
          onClick={onClose}
        />
      )}

      <aside className={`bg-charcoal-900 border-r border-charcoal-800 flex flex-col justify-between h-screen fixed md:sticky top-0 left-0 z-50 transition-all duration-300 ${
        isOpen ? 'translate-x-0 w-64' : '-translate-x-full md:translate-x-0'
      } ${isDesktopCollapsed ? 'md:w-20' : 'md:w-64'}`}>
        <div>
          {/* Brand Header */}
          <div className="p-5 flex items-center justify-between border-b border-charcoal-800 bg-charcoal-950/40 min-h-[73px]">
            <div className="flex items-center gap-3 overflow-hidden">
              <div className="h-10 w-10 shrink-0 rounded-lg bg-gradient-to-br from-gold-400 to-gold-600 flex items-center justify-center shadow-lg shadow-gold-500/10">
                <Zap className="h-5 w-5 text-charcoal-950 stroke-[2.5]" />
              </div>
              <div className={`transition-opacity duration-200 ${isDesktopCollapsed ? 'md:opacity-0 md:w-0' : 'opacity-100'}`}>
                <h1 className="font-extrabold text-lg tracking-wider text-white whitespace-nowrap">REAL.<span className="text-gold-500">i</span></h1>
                <p className="text-[10px] text-charcoal-400 font-semibold uppercase tracking-widest whitespace-nowrap">Meal Demand AI</p>
              </div>
            </div>
            
            {/* Desktop Collapse/Expand Control (< / >) */}
            <button 
              onClick={() => setIsDesktopCollapsed(!isDesktopCollapsed)}
              className="hidden md:flex h-7 w-7 rounded-lg bg-charcoal-800 border border-charcoal-700 text-gold-400 font-bold hover:text-white items-center justify-center cursor-pointer transition-colors"
              title={isDesktopCollapsed ? "Expand Sidebar" : "Collapse Sidebar"}
            >
              {isDesktopCollapsed ? '>' : '<'}
            </button>

            {/* Mobile Collapse/Close Control (^) */}
            <button 
              onClick={onClose}
              className="md:hidden h-8 w-8 rounded-lg bg-charcoal-800 border border-charcoal-700 text-gold-400 font-extrabold hover:text-white flex items-center justify-center cursor-pointer"
              title="Close Menu"
            >
              ^
            </button>
          </div>

          {/* Navigation Items */}
          <nav className="p-4 space-y-1.5 mt-4">
            {menuItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => {
                    setActiveTab(item.id);
                    onClose();
                  }}
                  className={`w-full flex items-center py-3 rounded-xl transition-all duration-250 font-medium text-sm group ${
                    isDesktopCollapsed ? 'md:justify-center px-0' : 'px-4'
                  } ${
                    isActive 
                      ? 'bg-gradient-to-r from-gold-500/10 to-transparent text-gold-400 border-l-3 border-gold-500 shadow-inner' 
                      : 'text-charcoal-300 hover:text-white hover:bg-charcoal-800/40'
                  }`}
                  title={isDesktopCollapsed ? item.name : undefined}
                >
                  <Icon className={`h-4.5 w-4.5 transition-transform duration-200 group-hover:scale-105 shrink-0 ${
                    isActive ? 'text-gold-500' : 'text-charcoal-400 group-hover:text-charcoal-200'
                  } ${isDesktopCollapsed ? 'md:mx-0' : 'mr-3.5'}`} />
                  <span className={`transition-opacity duration-200 ${isDesktopCollapsed ? 'md:hidden' : 'inline'}`}>
                    {item.name}
                  </span>
                </button>
              );
            })}
          </nav>
        </div>

        {/* Footer Info & Connection Status */}
        <div className="p-4 border-t border-charcoal-800 space-y-3.5 bg-charcoal-950/20">
          <div className={`flex items-center justify-between px-2 text-xs ${isDesktopCollapsed ? 'md:justify-center' : ''}`}>
            <span className={`text-charcoal-400 font-medium ${isDesktopCollapsed ? 'md:hidden' : 'inline'}`}>System Status</span>
            <div className="flex items-center gap-1.5 font-semibold">
              {isBackendConnected ? (
                <>
                  <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
                  <span className={`text-emerald-400 ${isDesktopCollapsed ? 'md:hidden' : 'inline'}`}>ONLINE</span>
                </>
              ) : (
                <>
                  <span className="h-2 w-2 rounded-full bg-amber-500" />
                  <span className={`text-amber-400 ${isDesktopCollapsed ? 'md:hidden' : 'inline'}`}>DEMO MODE</span>
                </>
              )}
            </div>
          </div>

          <div className={`flex items-center rounded-lg bg-charcoal-800/20 border border-charcoal-800/60 ${
            isDesktopCollapsed ? 'md:justify-center p-2' : 'px-3 py-2.5 gap-3'
          }`}>
            <div className="h-8 w-8 shrink-0 rounded-full bg-charcoal-800 flex items-center justify-center font-bold text-xs text-gold-400 border border-charcoal-700">
              AD
            </div>
            <div className={`overflow-hidden transition-opacity duration-200 ${isDesktopCollapsed ? 'md:hidden' : 'block'}`}>
              <p className="text-xs font-semibold text-charcoal-200 truncate">Administrator</p>
              <p className="text-[10px] text-charcoal-400 truncate">admin@real-i.com</p>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
}
