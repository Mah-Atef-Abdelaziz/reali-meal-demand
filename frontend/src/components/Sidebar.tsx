import React from 'react';
import { 
  LayoutDashboard, 
  TrendingUp, 
  MessageSquare, 
  FileText, 
  MenuSquare, 
  Settings, 
  Wifi, 
  WifiOff, 
  LogOut,
  Zap
} from 'lucide-react';

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  isBackendConnected: boolean;
}

export default function Sidebar({ activeTab, setActiveTab, isBackendConnected }: SidebarProps) {
  const menuItems = [
    { id: 'dashboard', name: 'Dashboard', icon: LayoutDashboard },
    { id: 'predictions', name: 'Predictions', icon: TrendingUp },
    { id: 'chatbot', name: 'Smart Assistant', icon: MessageSquare },
    { id: 'menus', name: 'Menu Planning', icon: MenuSquare },
    { id: 'reports', name: 'Reports & Logs', icon: FileText },
    { id: 'settings', name: 'System Settings', icon: Settings },
  ];

  return (
    <aside className="w-64 bg-charcoal-900 border-r border-charcoal-800 flex flex-col justify-between h-screen sticky top-0">
      <div>
        {/* Brand Header */}
        <div className="p-6 flex items-center gap-3 border-b border-charcoal-800 bg-charcoal-950/40">
          <div className="h-10 w-10 rounded-lg bg-gradient-to-br from-gold-400 to-gold-600 flex items-center justify-center shadow-lg shadow-gold-500/10">
            <Zap className="h-5 w-5 text-charcoal-950 stroke-[2.5]" />
          </div>
          <div>
            <h1 className="font-extrabold text-lg tracking-wider text-white">REAL.<span className="text-gold-500">i</span></h1>
            <p className="text-[10px] text-charcoal-400 font-semibold uppercase tracking-widest">Meal Demand AI</p>
          </div>
        </div>

        {/* Navigation Items */}
        <nav className="p-4 space-y-1.5 mt-4">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center gap-3.5 px-4 py-3 rounded-xl transition-all duration-250 font-medium text-sm group ${
                  isActive 
                    ? 'bg-gradient-to-r from-gold-500/10 to-transparent text-gold-400 border-l-3 border-gold-500 shadow-inner' 
                    : 'text-charcoal-300 hover:text-white hover:bg-charcoal-800/40'
                }`}
              >
                <Icon className={`h-4.5 w-4.5 transition-transform duration-200 group-hover:scale-105 ${
                  isActive ? 'text-gold-500' : 'text-charcoal-400 group-hover:text-charcoal-200'
                }`} />
                <span>{item.name}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Footer Info & Connection Status */}
      <div className="p-4 border-t border-charcoal-800 space-y-3.5 bg-charcoal-950/20">
        <div className="flex items-center justify-between px-2 text-xs">
          <span className="text-charcoal-400 font-medium">System Status</span>
          <div className="flex items-center gap-1.5 font-semibold">
            {isBackendConnected ? (
              <>
                <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
                <span className="text-emerald-400">ONLINE</span>
              </>
            ) : (
              <>
                <span className="h-2 w-2 rounded-full bg-amber-500" />
                <span className="text-amber-400">DEMO MODE</span>
              </>
            )}
          </div>
        </div>

        <div className="flex items-center gap-3 px-3 py-2.5 rounded-lg bg-charcoal-800/20 border border-charcoal-800/60">
          <div className="h-8 w-8 rounded-full bg-charcoal-800 flex items-center justify-center font-bold text-xs text-gold-400 border border-charcoal-700">
            AD
          </div>
          <div className="overflow-hidden">
            <p className="text-xs font-semibold text-charcoal-200 truncate">Administrator</p>
            <p className="text-[10px] text-charcoal-400 truncate">admin@real-i.com</p>
          </div>
        </div>
      </div>
    </aside>
  );
}
